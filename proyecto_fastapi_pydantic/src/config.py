"""
Configuraciones y constantes globales del servicio FastAPI.
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "telemetria_api.db"

# Metadatos del servicio
API_TITLE = "API de Monitoreo y Telemetría Mecatrónica"
API_DESCRIPTION = (
    "Microservicio REST desarrollado con **FastAPI** y **Pydantic v2** para la "
    "gestión de estaciones de sensores, adquisición de telemetría física y alertas de umbral."
)
API_VERSION = "1.0.0"
