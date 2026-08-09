"""
Colector de telemetría y procesador de cola asíncrona (Patrón Productor-Consumidor).
"""

import asyncio
import logging
import time
from typing import List, Dict, Any
from src.database import TelemetryDatabase

logger = logging.getLogger("TelemetryCollector")

class TelemetryCollector:
    """
    Administra la recepción de mediciones desde el asyncio.Queue y coordina
    su inserción por lotes (Batch Processing) hacia SQLite.
    """

    def __init__(
        self, 
        db: TelemetryDatabase, 
        queue: asyncio.Queue, 
        batch_size: int = 25, 
        flush_interval: float = 0.5
    ):
        self.db = db
        self.queue = queue
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.total_insertados = 0

    async def start_worker(self, stop_event: asyncio.Event):
        """
        Consumidor/Worker asíncrono que extrae elementos del Queue y realiza inserts masivos.
        """
        logger.info("Worker de persistencia SQLite iniciado.")
        buffer: List[Dict[str, Any]] = []
        ultimo_flush = time.time()

        while not stop_event.is_set() or not self.queue.empty():
            try:
                # Intentar obtener una lectura de la cola con timeout para chequear el flush interval
                medicion = await asyncio.wait_for(self.queue.get(), timeout=0.1)
                buffer.append(medicion)
                self.queue.task_done()
            except asyncio.TimeoutError:
                pass

            ahora = time.time()
            alcanzo_tamano = len(buffer) >= self.batch_size
            alcanzo_tiempo = (ahora - ultimo_flush) >= self.flush_interval and len(buffer) > 0
            sistema_deteniendose = stop_event.is_set() and len(buffer) > 0

            # Si se cumple alguna condición de vaciado (flush), insertar en SQLite
            if alcanzo_tamano or alcanzo_tiempo or sistema_deteniendose:
                insertados = await self.db.insert_batch(buffer)
                self.total_insertados += insertados
                ultimo_flush = ahora
                buffer.clear()

        # Vaciado final de remanentes en cola
        while not self.queue.empty():
            medicion = self.queue.get_nowait()
            buffer.append(medicion)
            self.queue.task_done()

        if buffer:
            insertados = await self.db.insert_batch(buffer)
            self.total_insertados += insertados
            buffer.clear()

        logger.info(f"Worker de persistencia finalizado. Total registros insertados: {self.total_insertados}")
