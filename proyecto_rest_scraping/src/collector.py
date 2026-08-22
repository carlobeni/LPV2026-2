"""
Servicio de recolección continua y monitoreo en tiempo real.
"""

import time
import logging
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from src.api_client import WeatherAPIClient
from src.scraper import NewsWebScraper
from src.database import TelemetryDatabase
from src.config import DEFAULT_FETCH_INTERVAL_SECONDS

logger = logging.getLogger(__name__)
console = Console()

class ContinuousDataCollector:
    """Orquestador de recolección continua periódica."""

    def __init__(self, interval: float = DEFAULT_FETCH_INTERVAL_SECONDS):
        self.interval = interval
        self.api_client = WeatherAPIClient()
        self.scraper = NewsWebScraper()
        self.db = TelemetryDatabase()

    def run_single_cycle(self, cycle_num: int) -> None:
        """Ejecuta un ciclo completo de adquisición (REST + Web Scraping) y persistencia."""
        console.print(f"[bold cyan]=== Ejecutando Ciclo #{cycle_num} ===");

        # 1. Consumo REST API
        try:
            weather_data = self.api_client.fetch_current_weather()
            row_id = self.db.insert_weather_telemetry(weather_data)
            console.print(
                f"[green][OK] [REST API][/green] Temperatura: [bold]{weather_data['temperatura']} °C[/bold] | "
                f"Viento: {weather_data['velocidad_viento']} km/h (DB Row ID: {row_id})"
            )
        except Exception as e:
            console.print(f"[bold red][ERROR] en REST API:[/bold red] {e}")

        # 2. Web Scraping
        try:
            headlines = self.scraper.scrape_top_headlines(limit=3)
            count = self.db.insert_scraped_bulletins(headlines)
            console.print(f"[green][OK] [Web Scraping][/green] Insertados {count} titulares extraídos de HTML.")
        except Exception as e:
            console.print(f"[bold red][ERROR] en Web Scraping:[/bold red] {e}")

        # 3. Estado de la Base de Datos
        count_api, count_scrape = self.db.get_stats()
        console.print(
            f"[dim]Persistencia acumulada en SQLite -> API: {count_api} filas | Scraping: {count_scrape} filas[/dim]\n"
        )

    def start_loop(self, max_cycles: Optional[int] = None) -> None:
        """
        Inicia el bucle de recolección continua.
        Si max_cycles es None, corre indefinidamente hasta interrupción manual (Ctrl+C).
        """
        console.print(Panel.fit(
            "[bold green]Iniciando Servicio de Recolección Continua[/bold green]\n"
            "• Adquisición: REST API (Open-Meteo) + Web Scraping (BeautifulSoup4)\n"
            "• Persistencia: SQLite (telemetry_scraping.db)\n"
            f"• Frecuencia: Cada {self.interval} segundos",
            title="Lenguaje de Programación Visual - FIUNA"
        ))

        cycle = 1
        try:
            while True:
                self.run_single_cycle(cycle)
                if max_cycles and cycle >= max_cycles:
                    console.print(f"[bold yellow]Finalizado límite de {max_cycles} ciclos.[/bold yellow]")
                    break
                time.sleep(self.interval)
                cycle += 1
        except KeyboardInterrupt:
            console.print("\n[bold magenta]Servicio detenido por el usuario.[/bold magenta]")
