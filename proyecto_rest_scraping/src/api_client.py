"""
Módulo para consumo estructurado de APIs REST.
"""

from typing import Dict, Any, Optional
import logging
import httpx
from src.config import OPEN_METEO_URL, LOCATION_PARAMS, TIMEOUT_SECONDS, HTTP_HEADERS

logger = logging.getLogger(__name__)

class WeatherAPIClient:
    """Cliente para la obtención de datos meteorológicos vía REST API."""

    def __init__(self, base_url: str = OPEN_METEO_URL, headers: Optional[Dict[str, str]] = None):
        self.base_url = base_url
        self.headers = headers or HTTP_HEADERS

    def fetch_current_weather(self) -> Dict[str, Any]:
        """
        Realiza una petición HTTP GET sincrónica a la API REST.
        Devuelve un diccionario estandarizado con la lectura actual.
        """
        try:
            with httpx.Client(headers=self.headers, timeout=TIMEOUT_SECONDS) as client:
                response = client.get(self.base_url, params=LOCATION_PARAMS)
                response.raise_for_status()
                payload = response.json()
                
                current = payload.get("current_weather", {})
                return {
                    "origen": "REST_API_OPEN_METEO",
                    "temperatura": float(current.get("temperature", 0.0)),
                    "velocidad_viento": float(current.get("windspeed", 0.0)),
                    "direccion_viento": float(current.get("winddirection", 0.0)),
                    "codigo_clima": int(current.get("weathercode", 0)),
                    "estado_http": response.status_code
                }
        except httpx.HTTPError as err:
            logger.error(f"Error en la petición REST API: {err}")
            raise RuntimeError(f"Fallo al conectar con REST API: {err}") from err
