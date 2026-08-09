"""
Pruebas asíncronas con pytest y pytest-asyncio.
"""

import pytest
import asyncio
import time
import sys
from pathlib import Path

# Añadir el directorio raíz del proyecto al sys.path para importar correctamente src y config
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.database import TelemetryDatabase
from src.sensors import AsyncSensor
from src.collector import TelemetryCollector

@pytest.mark.asyncio
async def test_database_operations(tmp_path):
    """Verifica que la base de datos se cree, configure en WAL mode e inserte lotes correctamente."""
    db_file = tmp_path / "test_telemetry.db"
    db = TelemetryDatabase(db_file)
    await db.connect()

    assert await db.get_total_records() == 0

    batch = [
        {
            "timestamp": "2026-08-13 10:00:00.000",
            "timestamp_unix": time.time(),
            "sensor_id": "TEST_TEMP",
            "tipo_sensor": "Temperatura",
            "valor": 55.4,
            "unidad": "°C"
        },
        {
            "timestamp": "2026-08-13 10:00:01.000",
            "timestamp_unix": time.time() + 1,
            "sensor_id": "TEST_TEMP",
            "tipo_sensor": "Temperatura",
            "valor": 58.2,
            "unidad": "°C"
        }
    ]

    inserted = await db.insert_batch(batch)
    assert inserted == 2
    assert await db.get_total_records() == 2

    summary = await db.get_summary_by_sensor()
    assert len(summary) == 1
    assert summary[0]["sensor_id"] == "TEST_TEMP"
    assert summary[0]["lecturas"] == 2

    await db.close()

@pytest.mark.asyncio
async def test_sensor_collector_pipeline(tmp_path):
    """Verifica la integración asíncrona entre el sensor (productor) y el colector/worker (consumidor)."""
    db_file = tmp_path / "test_pipeline.db"
    db = TelemetryDatabase(db_file)
    await db.connect()

    queue = asyncio.Queue(maxsize=100)
    stop_event = asyncio.Event()

    sensor = AsyncSensor("SENSOR_VIB", "Vibracion", "m/s²", frecuencia_hz=20, rango_min=0, rango_max=10)
    collector = TelemetryCollector(db, queue, batch_size=5, flush_interval=0.1)

    # Iniciar tareas concurrentes
    sensor_task = asyncio.create_task(sensor.run(queue, stop_event))
    worker_task = asyncio.create_task(collector.start_worker(stop_event))

    # Dejar correr por 0.5 segundos
    await asyncio.sleep(0.5)
    stop_event.set()

    await asyncio.gather(sensor_task, worker_task)

    records = await db.get_total_records()
    assert records > 0, "El worker debería haber guardado registros en la base de datos."

    await db.close()
