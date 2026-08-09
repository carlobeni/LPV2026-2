# Proyecto Mecatrónico: Telemetría Asíncrona con Asyncio y SQLite

Este proyecto demuestra la implementación de un sistema de adquisición y persistencia de telemetría mecatrónica multicanal en tiempo real, utilizando **Asyncio** para la concurrencia I/O y **SQLite (aiosqlite)** optimizado en modo **WAL (Write-Ahead Logging)** para la persistencia temporal. La gestión de dependencias y empaquetado del proyecto se realiza mediante **Poetry** integrado sobre el entorno virtual de la asignatura (`lpv2026-2`).

---

## 🛠️ Arquitectura del Sistema

```
[ Sensor Temp (5 Hz) ] ──┐
[ Sensor Pres (10 Hz)] ──┼──> [ asyncio.Queue ] ──> [ Collector Worker ] ──> [ SQLite WAL (aiosqlite) ]
[ Sensor Vib  (20 Hz)] ──┘    (Buffer Circular)      (Batch Insert)            (telemetry_mechatronics.db)
```

- **Sensores Asíncronos (`src/sensors.py`)**: Corrutinas no bloqueantes que simulan la captura física con frecuencias variables (hasta 20 Hz) y ruido gaussiano.
- **Cola Asíncrona (`asyncio.Queue`)**: Desacopla la alta velocidad de transmisión de los sensores de las operaciones de escritura en disco.
- **Colector / Worker (`src/collector.py`)**: Consumidor asíncrono que procesa la cola en lotes (*batching*) para maximizar el rendimiento I/O.
- **Persistencia Temporal (`src/database.py`)**: Manejador de la base de datos SQLite asíncrona con índices estructurados por sensor y timestamp.

---

## 🚀 Requisitos e Instalación con Poetry

1. **Activar el entorno virtual de la asignatura:**
   ```bash
   conda activate lpv2026-2
   ```

2. **Instalar todas las dependencias del proyecto con Poetry:**
   Navegue al directorio del proyecto y ejecute `poetry install`:
   ```bash
   cd proyecto_sqlite_asyncio
   poetry install
   ```

   > **Nota:** `poetry install` leerá el archivo [`pyproject.toml`](file:///d:/Materiales%20de%20Auxiliar/1.%20Lenguaje%20de%20Programacion%20Visual/proyecto_sqlite_asyncio/pyproject.toml) e instalará automáticamente todas las dependencias requeridas (incluyendo las herramientas de desarrollo como `pytest` e `ipykernel`) dentro del entorno virtual.

---

## 💻 Instrucciones de Ejecución

### 1. Ejecutar la Simulación Principal
```bash
poetry run python main.py
```

### 2. Ejecutar Pruebas Automatizadas
```bash
poetry run pytest tests/
```

---

## 📊 Estructura del Proyecto (`pyproject.toml`)

- `pyproject.toml`: Archivo de configuración central de Poetry con las dependencias y metadatos del proyecto.
- `config/settings.py`: Configuración global (rutas DB, frecuencias, batch size).
- `src/database.py`: Gestor SQLite con `aiosqlite`.
- `src/sensors.py`: Generador de datos físicos multicanal.
- `src/collector.py`: Worker de consumo por lotes.
- `src/utils.py`: Visualización de tablas y resúmenes estadísticos.
- `data/`: Almacenamiento local del archivo `.db`.
- `tests/`: Pruebas de integración asíncronas (`test_telemetry.py`).
