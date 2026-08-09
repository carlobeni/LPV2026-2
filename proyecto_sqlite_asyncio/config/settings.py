"""
Configuración global del sistema de telemetría asíncrona y persistencia en SQLite.
"""

from pathlib import Path

# Directorio raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Ruta de la base de datos SQLite
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "telemetry_mechatronics.db"

# Parámetros del Buffer y Concurrencia
QUEUE_MAX_SIZE = 1000        # Máximo de mediciones en memoria (asyncio.Queue)
BATCH_SIZE = 25              # Cantidad de mediciones por lote para inserción masiva
WORKER_FLUSH_INTERVAL = 0.5   # Tiempo máximo en segundos para forzar inserción de lote parcial

# Configuración de Sensores Simulados (Frecuencia de muestreo en segundos)
SENSOR_CONFIGS = [
    {
        "sensor_id": "TEMP_MOTOR_01",
        "tipo": "Temperatura",
        "unidad": "°C",
        "frecuencia_hz": 5.0,     # 5 Hz (cada 0.2s)
        "rango_min": 45.0,
        "rango_max": 85.0,
        "ruido_std": 0.5
    },
    {
        "sensor_id": "PRES_HIDRAULICA_01",
        "tipo": "Presion",
        "unidad": "bar",
        "frecuencia_hz": 10.0,    # 10 Hz (cada 0.1s)
        "rango_min": 120.0,
        "rango_max": 180.0,
        "ruido_std": 1.2
    },
    {
        "sensor_id": "VIB_ROBOT_AXIS3",
        "tipo": "Vibracion",
        "unidad": "m/s²",
        "frecuencia_hz": 20.0,    # 20 Hz (cada 0.05s)
        "rango_min": 0.1,
        "rango_max": 3.5,
        "ruido_std": 0.15
    }
]
