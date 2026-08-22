"""
Configuración global del sistema de recolección continua y persistencia.
"""

from pathlib import Path

# Directorio raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Ruta de la Base de Datos SQLite
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "telemetry_scraping.db"

# Parámetros de APIs REST
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
LOCATION_PARAMS = {
    "latitude": -25.2637,  # Asunción, Paraguay (FIUNA)
    "longitude": -57.5759,
    "current_weather": True
}

# Parámetros de Web Scraping
SCRAPING_TARGET_URL = "https://news.ycombinator.com/"
HTTP_HEADERS = {
    "User-Agent": "MecatronicaBot/1.0 (FIUNA Educational Telemetry System; cbenitez@fiuna.edu.py)"
}

# Configuración del Monitor Continuo
DEFAULT_FETCH_INTERVAL_SECONDS = 5.0
MAX_RETRIES = 3
TIMEOUT_SECONDS = 8.0
