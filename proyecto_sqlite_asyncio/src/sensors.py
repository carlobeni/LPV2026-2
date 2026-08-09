"""
Simulador de sensores mecatrónicos basados en corrutinas de asyncio.
"""

import asyncio
import random
import time
import logging
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger("AsyncSensors")

class AsyncSensor:
    """
    Representa un sensor físico mecatrónico que adquiere datos en segundo plano
    y los envía a una cola compartida (asyncio.Queue).
    """

    def __init__(
        self, 
        sensor_id: str, 
        tipo: str, 
        unidad: str, 
        frecuencia_hz: float, 
        rango_min: float, 
        rango_max: float, 
        ruido_std: float = 0.5
    ):
        self.sensor_id = sensor_id
        self.tipo = tipo
        self.unidad = unidad
        self.intervalo = 1.0 / frecuencia_hz
        self.rango_min = rango_min
        self.rango_max = rango_max
        self.ruido_std = ruido_std
        self._running = False
        self._valor_base = (rango_min + rango_max) / 2.0

    async def run(self, queue: asyncio.Queue, stop_event: asyncio.Event):
        """
        Ciclo principal del sensor asíncrono.
        Genera lecturas según la frecuencia especificada y las deposita en el Queue.
        """
        self._running = True
        logger.info(f"Sensor [{self.sensor_id}] iniciado a {1.0/self.intervalo:.1f} Hz.")

        while not stop_event.is_set():
            # Simular fluctuación física (paseo aleatorio suave con ruido gaussiano)
            variacion = random.gauss(0, self.ruido_std)
            self._valor_base = max(self.rango_min, min(self.rango_max, self._valor_base + variacion))

            ahora = time.time()
            dt_iso = datetime.fromtimestamp(ahora).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

            medicion = {
                "timestamp": dt_iso,
                "timestamp_unix": ahora,
                "sensor_id": self.sensor_id,
                "tipo_sensor": self.tipo,
                "valor": round(self._valor_base, 3),
                "unidad": self.unidad
            }

            try:
                # Depositar en la cola sin bloquear indefinidamente si está llena
                queue.put_nowait(medicion)
            except asyncio.QueueFull:
                logger.warning(f"Búfer lleno! Lectura descartada en sensor [{self.sensor_id}]")

            # Liberar el Event Loop durante el intervalo de muestreo
            await asyncio.sleep(self.intervalo)

        self._running = False
        logger.info(f"Sensor [{self.sensor_id}] detenido.")
