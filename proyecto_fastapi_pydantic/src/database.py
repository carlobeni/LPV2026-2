"""
Capa de persistencia con SQLite para la API de Telemetría.
"""
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Dict, Any
from src.config import DB_PATH
from src.models import SensorCreate, LecturaCreate


class DatabaseManager:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        if self.db_path != Path(":memory:"):
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def init_db(self):
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sensores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    tipo TEXT NOT NULL,
                    ubicacion TEXT NOT NULL,
                    unidad TEXT NOT NULL,
                    umbral_alerta REAL NOT NULL,
                    activo BOOLEAN NOT NULL DEFAULT 1,
                    creado_en TIMESTAMP NOT NULL
                );
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS lecturas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sensor_id INTEGER NOT NULL,
                    valor REAL NOT NULL,
                    unidad TEXT NOT NULL,
                    alerta_activa BOOLEAN NOT NULL,
                    observacion TEXT,
                    timestamp TIMESTAMP NOT NULL,
                    FOREIGN KEY (sensor_id) REFERENCES sensores(id) ON DELETE CASCADE
                );
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_lecturas_sensor ON lecturas(sensor_id, timestamp);")
            conn.commit()

    def crear_sensor(self, data: SensorCreate) -> Dict[str, Any]:
        ahora = datetime.now(timezone.utc).isoformat()
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO sensores (nombre, tipo, ubicacion, unidad, umbral_alerta, activo, creado_en)
                VALUES (?, ?, ?, ?, ?, 1, ?)
            """, (data.nombre, data.tipo.value, data.ubicacion, data.unidad, data.umbral_alerta, ahora))
            sensor_id = cur.lastrowid
            conn.commit()
            return self.obtener_sensor(sensor_id)

    def obtener_sensores(self, tipo: Optional[str] = None, activo: Optional[bool] = None) -> List[Dict[str, Any]]:
        query = "SELECT * FROM sensores WHERE 1=1"
        params = []
        if tipo:
            query += " AND tipo = ?"
            params.append(tipo)
        if activo is not None:
            query += " AND activo = ?"
            params.append(1 if activo else 0)
        query += " ORDER BY id ASC;"

        with self.get_connection() as conn:
            cur = conn.cursor()
            rows = cur.execute(query, params).fetchall()
            return [dict(r) for r in rows]

    def obtener_sensor(self, sensor_id: int) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cur = conn.cursor()
            row = cur.execute("SELECT * FROM sensores WHERE id = ?", (sensor_id,)).fetchone()
            return dict(row) if row else None

    def eliminar_sensor(self, sensor_id: int) -> bool:
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM sensores WHERE id = ?", (sensor_id,))
            conn.commit()
            return cur.rowcount > 0

    def registrar_lectura(self, sensor_id: int, data: LecturaCreate) -> Optional[Dict[str, Any]]:
        sensor = self.obtener_sensor(sensor_id)
        if not sensor or not sensor["activo"]:
            return None

        alerta_activa = data.valor > sensor["umbral_alerta"]
        ahora = datetime.now(timezone.utc).isoformat()

        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO lecturas (sensor_id, valor, unidad, alerta_activa, observacion, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (sensor_id, data.valor, sensor["unidad"], 1 if alerta_activa else 0, data.observacion, ahora))
            lectura_id = cur.lastrowid
            conn.commit()

            row = cur.execute("SELECT * FROM lecturas WHERE id = ?", (lectura_id,)).fetchone()
            return dict(row)

    def obtener_lecturas(self, sensor_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cur = conn.cursor()
            rows = cur.execute("""
                SELECT * FROM lecturas 
                WHERE sensor_id = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (sensor_id, limit)).fetchall()
            return [dict(r) for r in rows]

    def obtener_resumen(self, sensor_id: int) -> Optional[Dict[str, Any]]:
        sensor = self.obtener_sensor(sensor_id)
        if not sensor:
            return None

        with self.get_connection() as conn:
            cur = conn.cursor()
            stats = cur.execute("""
                SELECT 
                    COUNT(*) as total,
                    AVG(valor) as promedio,
                    MIN(valor) as minimo,
                    MAX(valor) as maximo,
                    SUM(CASE WHEN alerta_activa = 1 THEN 1 ELSE 0 END) as alertas
                FROM lecturas
                WHERE sensor_id = ?
            """, (sensor_id,)).fetchone()

            return {
                "sensor": sensor,
                "total_lecturas": stats["total"] or 0,
                "promedio_valor": round(stats["promedio"], 2) if stats["promedio"] is not None else None,
                "minimo_valor": stats["minimo"],
                "maximo_valor": stats["maximo"],
                "alertas_registradas": stats["alertas"] or 0
            }


# Instancia singleton para uso en inyección de dependencias
db_manager = DatabaseManager()


def get_db() -> DatabaseManager:
    return db_manager
