"""
Utilidades auxiliares para formateo y despliegue de reportes de telemetría.
"""

from typing import List, Dict, Any

try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False

def imprimir_resumen_sensores(resumen: List[Dict[str, Any]]):
    """Muestra una tabla formateada en consola con el resumen estadístico de los sensores."""
    if not resumen:
        print("No hay datos de sensores para mostrar.")
        return

    print("\n" + "=" * 80)
    print("           RESUMEN ESTADÍSTICO DE TELEMETRÍA PERSISTIDA EN SQLITE")
    print("=" * 80)

    if HAS_TABULATE:
        headers = {
            "sensor_id": "ID Sensor",
            "tipo_sensor": "Tipo",
            "unidad": "Unidad",
            "lecturas": "Cant. Lecturas",
            "promedio": "Promedio",
            "minimo": "Mínimo",
            "maximo": "Máximo"
        }
        # Reestructurar datos para la tabla
        filas = []
        for r in resumen:
            filas.append([
                r["sensor_id"],
                r["tipo_sensor"],
                r["unidad"],
                r["lecturas"],
                f"{r['promedio']:.3f}",
                f"{r['minimo']:.3f}",
                f"{r['maximo']:.3f}"
            ])
        headers_list = ["Sensor ID", "Tipo", "Unidad", "Lecturas", "Promedio", "Mínimo", "Máximo"]
        print(tabulate(filas, headers=headers_list, tablefmt="fancy_grid"))
    else:
        print(f"{'Sensor ID':<20} | {'Tipo':<12} | {'Lecturas':<10} | {'Promedio':<10} | {'Min':<8} | {'Max':<8}")
        print("-" * 75)
        for r in resumen:
            print(f"{r['sensor_id']:<20} | {r['tipo_sensor']:<12} | {r['lecturas']:<10} | {r['promedio']:<10} | {r['minimo']:<8} | {r['maximo']:<8}")
    print("=" * 80 + "\n")

def imprimir_ultimas_lecturas(lecturas: List[Dict[str, Any]]):
    """Muestra las últimas lecturas capturadas por el sistema."""
    if not lecturas:
        print("No se registraron lecturas recientes.")
        return

    print("\n--- MUESTRA DE ÚLTIMAS 10 LECTURAS INGRESADAS EN SQLITE ---")
    for row in lecturas:
        print(f"[{row['timestamp']}] {row['sensor_id']} ({row['tipo_sensor']}): {row['valor']} {row['unidad']}")
    print("-" * 60)
