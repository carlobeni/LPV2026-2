"""
Módulo de Web Scraping para extracción sintáctica de datos en documentos HTML.
"""

from typing import List, Dict, Any, Optional
import logging
import httpx
from bs4 import BeautifulSoup
from src.config import SCRAPING_TARGET_URL, HTTP_HEADERS, TIMEOUT_SECONDS

logger = logging.getLogger(__name__)

class NewsWebScraper:
    """Scraper sintáctico basado en BeautifulSoup4 y Selectores CSS."""

    def __init__(self, target_url: str = SCRAPING_TARGET_URL, headers: Optional[Dict[str, str]] = None):
        self.target_url = target_url
        self.headers = headers or HTTP_HEADERS

    def scrape_top_headlines(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Consulta la página HTML objetivo y extrae los primeros N titulares con sus enlaces.
        """
        results = []
        try:
            with httpx.Client(headers=self.headers, timeout=TIMEOUT_SECONDS, follow_redirects=True) as client:
                response = client.get(self.target_url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, "html.parser")
                # Selección con selector CSS
                links = soup.select(".titleline > a")
                
                for idx, link in enumerate(links[:limit], start=1):
                    title = link.get_text(strip=True)
                    url = link.get("href", "")
                    results.append({
                        "posicion": idx,
                        "titulo": title,
                        "url": url,
                        "longitud_titulo": len(title)
                    })
                return results
        except Exception as err:
            logger.error(f"Error durante la extracción Web Scraping: {err}")
            return results
