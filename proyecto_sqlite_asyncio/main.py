"""
Punto de entrada principal para el Sistema de Telemetría Mecatrónica con Asyncio y SQLite.
"""

import asyncio
import logging
import time
import sys
from pathlib import Path

# Ajustar PYTHONPATH
sys.path.insert(0, str(Path(__file__).resolve().parent))

from config.settings import DB_PATH, QUEUE_MAX_SIZE, BATCH_SIZE, WORKER_FLUSH_INTERVAL, SENSOR_CONFIGS
from src.database import TelemetryDatabase
from src.sensors import AsyncSensor
from src.collector import TelemetryCollector
from src.utils import imprimir_resumen_sensores, imprimir_ultimas_lecturas

# Configurar Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("Main")

async def main(duracion_simulacion_seg: float = 6.0):
    """
    Función asíncrona principal:
    1. Inicializa la base de datos SQLite en modo WAL.
    2. Instancia los sensores mecatrónicos y el worker de persistencia.
    3. Ejecuta las corrutinas concurrentes durante la duración especificada.
    4. Muestra reportes y realiza el apagado limpio del sistema.
    """
    logger.info("=== INICIANDO SISTEMA DE TELEMETRÍA MECATRÓNICA (ASYNCIO + SQLITE) ===")
    
    # 1. Base de datos
    db = TelemetryDatabase(DB_PATH)
    await db.connect()

    # 2. Cola asíncrona y evento de detención
    queue: asyncio.Queue = asyncio.Queue(maxsize=QUEUE_MAX_SIZE)
    stop_event = asyncio.Event()

    # 3. Crear instancias de sensores
    sensores = [
        AsyncSensor(
            sensor_id=cfg["sensor_id"],
            tipo=cfg["tipo"],
            unidad=cfg["unidad"],
            frecuencia_hz=cfg["frecuencia_hz"],
            rango_min=cfg["rango_min"],
            rango_max=cfg["rango_max"],
            ruido_std=cfg["ruido_std"]
        )
        for cfg in SENSOR_CONFIGS
    ]

    # 4. Crear colector/worker
    collector = TelemetryCollector(
        db=db,
        queue=queue,
        batch_size=BATCH_SIZE,
        flush_interval=WORKER_FLUSH_INTERVAL
    )

    # 5. Desplegar corrutinas concurrentes
    tasks = []
    for s in sensores:
        t = asyncio.create_task(s.run(queue, stop_event))
        tasks.append(t)

    worker_task = asyncio.create_task(collector.start_worker(stop_event))
    tasks.append(worker_task)

    logger.info(f"Sistema corriendo concurrentemente. Duración de la simulación: {duracion_simulacion_seg} segundos...")

    try:
        # Esperar la duración de la simulación
        await asyncio.sleep(duracion_simulacion_seg)
    except KeyboardInterrupt:
        logger.warning("Interrupción detectada por teclado (Ctrl+C). Iniciando apagado...")
    finally:
        # Señalizar apagado a las corrutinas
        stop_event.set()
        
        # Esperar la finalización ordenada de todos los generadores y el worker
        await asyncio.gather(*tasks)

        logger.info("=== SIMULACIÓN COMPLETADA ===")

        # 6. Consultar y presentar resultados desde SQLite
        total = await db.get_total_records()
        logger.info(f"Total histórico de registros en SQLite: {total}")

        resumen = await db.get_summary_by_sensor()
        imprimir_resumen_sensores(resumen)

        ultimas = await db.fetch_recent(10)
        imprimir_ultimas_lecturas(ultimas)

        # 7. Cerrar conexión
        await db.close()

if __name__ == "__main__":
    # Ejecutar el bucle de eventos de asyncio
    asyncio.run(main(duracion_simulacion_seg=6.0))
