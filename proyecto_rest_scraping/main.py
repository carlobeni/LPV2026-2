"""
Punto de entrada principal para el servicio de recolección continua de datos.
"""

import sys
import argparse
from src.collector import ContinuousDataCollector
from src.config import DEFAULT_FETCH_INTERVAL_SECONDS

def main():
    parser = argparse.ArgumentParser(description="Sistema de Telemetría Continua REST API + Web Scraping")
    parser.add_argument(
        "--interval",
        type=float,
        default=DEFAULT_FETCH_INTERVAL_SECONDS,
        help="Intervalo entre ciclos de recolección en segundos"
    )
    parser.add_argument(
        "--cycles",
        type=int,
        default=None,
        help="Número máximo de ciclos a ejecutar (por defecto: indefinido)"
    )
    
    args = parser.parse_args()

    collector = ContinuousDataCollector(interval=args.interval)
    collector.start_loop(max_cycles=args.cycles)

if __name__ == "__main__":
    main()
