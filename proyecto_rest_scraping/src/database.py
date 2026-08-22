"""
Capa de Persistencia Relacional en SQLite.
"""

from typing import List, Dict, Any, Tuple
import sqlite3
import logging
from pathlib import Path
from src.config import DB_PATH

logger = logging.getLogger(__name__)

class TelemetryDatabase:
    """Manejador de la base de datos relacional SQLite."""

    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        """Inicializa las tablas relacionales e índices."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Tabla 1: Telemetría obtenida por REST API
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS api_telemetry_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                origen TEXT NOT NULL,
                temperatura REAL NOT NULL,
                velocidad_viento REAL NOT NULL,
                direccion_viento REAL NOT NULL,
                codigo_clima INTEGER NOT NULL,
                estado_http INTEGER NOT NULL,
                registrado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)
            
            # Tabla 2: Titulares y boletines extraídos mediante Web Scraping
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS scraped_bulletins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                posicion INTEGER NOT NULL,
                titulo TEXT NOT NULL,
                url TEXT NOT NULL,
                longitud_titulo INTEGER NOT NULL,
                registrado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)
            
            # Índices temporales
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_api_fecha ON api_telemetry_logs(registrado_en);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_scrape_fecha ON scraped_bulletins(registrado_en);")
            conn.commit()

    def insert_weather_telemetry(self, data: Dict[str, Any]) -> int:
        """Inserta un registro de telemetría proveniente de REST API."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO api_telemetry_logs 
            (origen, temperatura, velocidad_viento, direccion_viento, codigo_clima, estado_http)
            VALUES (?, ?, ?, ?, ?, ?);
            """, (
                data["origen"],
                data["temperatura"],
                data["velocidad_viento"],
                data["direccion_viento"],
                data["codigo_clima"],
                data["estado_http"]
            ))
            conn.commit()
            return cursor.lastrowid

    def insert_scraped_bulletins(self, items: List[Dict[str, Any]]) -> int:
        """Inserta un lote de titulares procesados mediante Web Scraping."""
        inserted_count = 0
        with self._get_connection() as conn:
            cursor = conn.cursor()
            for item in items:
                cursor.execute("""
                INSERT INTO scraped_bulletins 
                (posicion, titulo, url, longitud_titulo)
                VALUES (?, ?, ?, ?);
                """, (
                    item["posicion"],
                    item["titulo"],
                    item["url"],
                    item["longitud_titulo"]
                ))
                inserted_count += 1
            conn.commit()
        return inserted_count

    def get_stats(self) -> Tuple[int, int]:
        """Retorna el conteo total de registros en ambas tablas (api_records, scrape_records)."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM api_telemetry_logs;")
            count_api = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM scraped_bulletins;")
            count_scrape = cursor.fetchone()[0]
            return count_api, count_scrape
