"""
Gestor de persistencia asíncrona en SQLite con aiosqlite y soporte para series temporales.
"""

import aiosqlite
import logging
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

logger = logging.getLogger("TelemetryDB")

class TelemetryDatabase:
    """
    Administra la base de datos SQLite asíncrona optimizada para alta frecuencia de lectura I/O
    mediante el modo WAL (Write-Ahead Logging) y transacciones por lotes (batch inserts).
    """

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn: Optional[aiosqlite.Connection] = None

    async def connect(self):
        """Abre la conexión e inicializa PRAGMAs de alto rendimiento y el esquema de tablas."""
        self._conn = await aiosqlite.connect(self.db_path)
        self._conn.row_factory = aiosqlite.Row

        # Habilitar WAL mode para permitir lecturas y escrituras concurrentes sin bloqueos de tabla
        await self._conn.execute("PRAGMA journal_mode = WAL;")
        await self._conn.execute("PRAGMA synchronous = NORMAL;")
        await self._conn.execute("PRAGMA temp_store = MEMORY;")

        await self._create_tables()
        logger.info(f"Conexión a SQLite establecida (WAL mode activo) en: {self.db_path}")

    async def _create_tables(self):
        """Crea la tabla de telemetría e índices temporales optimizados."""
        query_table = """
        CREATE TABLE IF NOT EXISTS lecturas_telemetria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME NOT NULL,
            timestamp_unix REAL NOT NULL,
            sensor_id TEXT NOT NULL,
            tipo_sensor TEXT NOT NULL,
            valor REAL NOT NULL,
            unidad TEXT NOT NULL
        );
        """
        
        # Índices para acelerar consultas por sensor y rango de tiempo
        query_idx1 = """
        CREATE INDEX IF NOT EXISTS idx_sensor_time 
        ON lecturas_telemetria (sensor_id, timestamp_unix);
        """
        
        query_idx2 = """
        CREATE INDEX IF NOT EXISTS idx_timestamp 
        ON lecturas_telemetria (timestamp_unix);
        """

        if self._conn:
            await self._conn.execute(query_table)
            await self._conn.execute(query_idx1)
            await self._conn.execute(query_idx2)
            await self._conn.commit()

    async def insert_batch(self, batch: List[Dict[str, Any]]) -> int:
        """
        Inserta un lote de mediciones dentro de una única transacción atómica asíncrona.
        Retorna la cantidad de registros insertados.
        """
        if not batch or not self._conn:
            return 0

        query = """
        INSERT INTO lecturas_telemetria 
        (timestamp, timestamp_unix, sensor_id, tipo_sensor, valor, unidad)
        VALUES (:timestamp, :timestamp_unix, :sensor_id, :tipo_sensor, :valor, :unidad);
        """
        
        try:
            await self._conn.executemany(query, batch)
            await self._conn.commit()
            return len(batch)
        except Exception as e:
            await self._conn.rollback()
            logger.error(f"Error al insertar lote en SQLite: {e}")
            raise e

    async def get_total_records(self) -> int:
        """Retorna la cantidad total de registros en la base de datos."""
        if not self._conn:
            return 0
        async with self._conn.execute("SELECT COUNT(*) as total FROM lecturas_telemetria;") as cursor:
            row = await cursor.fetchone()
            return row["total"] if row else 0

    async def get_summary_by_sensor(self) -> List[Dict[str, Any]]:
        """Retorna estadísticas descriptivas (Promedio, Mínimo, Máximo, Conteos) agrupadas por sensor."""
        if not self._conn:
            return []
            
        query = """
        SELECT 
            sensor_id,
            tipo_sensor,
            unidad,
            COUNT(*) as lecturas,
            ROUND(AVG(valor), 3) as promedio,
            ROUND(MIN(valor), 3) as minimo,
            ROUND(MAX(valor), 3) as maximo
        FROM lecturas_telemetria
        GROUP BY sensor_id;
        """
        async with self._conn.execute(query) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def fetch_recent(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retorna las últimas 'limit' mediciones registradas."""
        if not self._conn:
            return []
            
        query = """
        SELECT timestamp, sensor_id, tipo_sensor, valor, unidad 
        FROM lecturas_telemetria 
        ORDER BY id DESC 
        LIMIT ?;
        """
        async with self._conn.execute(query, (limit,)) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def close(self):
        """Cierra de forma limpia la conexión a la base de datos."""
        if self._conn:
            await self._conn.close()
            logger.info("Conexión a SQLite cerrada correctamente.")
            self._conn = None
