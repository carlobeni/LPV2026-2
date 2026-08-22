"""
Pruebas unitarias con pytest.
"""

import pytest
import sqlite3
from pathlib import Path
from src.api_client import WeatherAPIClient
from src.scraper import NewsWebScraper
from src.database import TelemetryDatabase

def test_database_initialization(tmp_path: Path):
    test_db_path = tmp_path / "test_telemetry.db"
    db = TelemetryDatabase(db_path=test_db_path)
    
    assert test_db_path.exists()
    
    count_api, count_scrape = db.get_stats()
    assert count_api == 0
    assert count_scrape == 0

def test_insert_weather_telemetry(tmp_path: Path):
    test_db_path = tmp_path / "test_telemetry.db"
    db = TelemetryDatabase(db_path=test_db_path)
    
    mock_data = {
        "origen": "TEST_REST_API",
        "temperatura": 25.5,
        "velocidad_viento": 12.0,
        "direccion_viento": 180.0,
        "codigo_clima": 1,
        "estado_http": 200
    }
    
    row_id = db.insert_weather_telemetry(mock_data)
    assert row_id > 0
    
    count_api, _ = db.get_stats()
    assert count_api == 1

def test_insert_scraped_bulletins(tmp_path: Path):
    test_db_path = tmp_path / "test_telemetry.db"
    db = TelemetryDatabase(db_path=test_db_path)
    
    mock_items = [
        {"posicion": 1, "titulo": "Titular 1", "url": "https://example.com/1", "longitud_titulo": 9},
        {"posicion": 2, "titulo": "Titular 2", "url": "https://example.com/2", "longitud_titulo": 9}
    ]
    
    inserted = db.insert_scraped_bulletins(mock_items)
    assert inserted == 2
    
    _, count_scrape = db.get_stats()
    assert count_scrape == 2
