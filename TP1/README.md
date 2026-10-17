# Trabajo Práctico 1 (TP1) — Extracción de Datos, Persistencia y API REST

### Lenguajes de Programación Visual (Código: 5728)
**Ingeniería Mecatrónica — Facultad de Ingeniería, Universidad Nacional de Asunción (FIUNA)**  
**Primer Ciclo 2026**  
**Profesor Titular:** Ing. Jorge Luis Tillería Mereles  
**Auxiliar de Práctica:** Ing. Carlos María Benítez Cardozo  

---

## Información del Trabajo Práctico

| Parámetro | Detalle |
|---|---|
| **Ponderación** | 5 puntos del proceso acumulado |
| **Periodo de Desarrollo** | Semanas 1 a 4 |
| **Fecha Límite de Entrega** | Semana 4 (Cierre de Unidad 2 - Web Scraping y REST) |
| **Modalidad** | Grupal (según conformación del proyecto final) |
| **Repositorio** | Rama de trabajo dedicada o repositorio del equipo |

---

## Requerimientos de Entrega

Para la entrega se requiere:
1. Extracción de datos a través de scraping de datos o consumo de una API
2. Guardado de la información en una base de datos
3. Disponibilización de la manipulación de la información a través de una API propia desarrollada en FastAPI

El lugar de extracción de datos se definirá según el proyecto final elegido en el foro.

---

## 1. Alcance Técnico y Especificaciones

### 1.1 Extracción de Datos (Scraping o Consumo de API Externa)
- **Opción A — Web Scraping:**
  - Extraer información de interés mecatrónico o temático desde sitios web públicos empleando librerías especializadas de Python (`BeautifulSoup4`, `httpx`, `requests` o `lxml`).
  - Implementar manejo de excepciones por caída de conexión, *timeouts* y headers de solicitud (`User-Agent`).
  - La extracción debe estructurarse mediante funciones o clases desacopladas (ej. `scraper.py`).
- **Opción B — Consumo de API Externa:**
  - Consumo programático de una API web pública o de telemetría (REST, JSON) mediante peticiones HTTP asíncronas o síncronas.
  - Transformación y saneamiento de los datos obtenidos antes del almacenamiento.

### 1.2 Persistencia en Base de Datos
- **Motor de Base de Datos:** SQLite (recomendado para desarrollo local) o PostgreSQL (local / Supabase).
- **Modelado:**
  - Definir un esquema estructurado con al menos una tabla principal que almacene los datos recolectados.
  - Incluir campos obligatorios: clave primaria (`id`), datos cuantitativos o cualitativos extraídos, y marca de tiempo (`timestamp` de inserción).
- **Integridad:**
  - Mecanismo automático de inicialización de tablas (ej. `init_db.py` o migraciones).
  - Prevención de duplicados mediante índices únicos o validación previa.

### 1.3 Disponibilización mediante API propia con FastAPI
- **Framework:** `FastAPI` con validación estricta de esquemas mediante `Pydantic v2`.
- **Endpoints Mínimos Requeridos:**
  - `GET /`: Mensaje de bienvenida y estado operativo del servicio.
  - `GET /items` (o recurso correspondiente): Listado paginado o con parámetros de búsqueda/filtrado (`searchParams`).
  - `GET /items/{id}`: Búsqueda individual por identificador con retorno HTTP 404 si no existe.
  - `POST /items`: Inserción manual de nuevos registros validada con esquema Pydantic.
  - `POST /scrape` o `POST /sincronizar`: Endpoint que dispare el proceso de extracción y guardado en la base de datos.
  - `DELETE /items/{id}` o `PUT /items/{id}`: Operación de borrado o actualización de registros existentes.
- **Documentación Interactiva:**
  - Swagger UI habilitado automáticamente en `/docs`.
  - Redoc disponible en `/redoc`.

---

## 2. Estructura de Proyecto Recomendada

```
tp1-proyecto/
├── database.py              <- Conexión y gestión de sesiones de base de datos
├── init_db.py               <- Script DDL para inicializar tablas y esquemas
├── main.py                  <- Aplicación FastAPI y definición de endpoints
├── schemas.py               <- Modelos Pydantic v2 para validación de entrada/salida
├── scraper.py               <- Módulo de extracción y parsing (Scraping / API externa)
├── pyproject.toml / req.txt <- Gestión de dependencias (FastAPI, uvicorn, pydantic, bs4, httpx)
└── README.md                <- Documentación del proyecto, fuentes de datos y cómo ejecutar
```

---

## 3. Instrucciones de Ejecución

1. Clonar el repositorio y posicionarse en la carpeta del proyecto.
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   # O con poetry:
   poetry install
   ```
3. Inicializar la base de datos:
   ```bash
   python init_db.py
   ```
4. Iniciar el servidor local FastAPI:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
5. Acceder a la documentación interactiva en el navegador:
   👉 **`http://localhost:8000/docs`**

---

## 4. Criterios de Evaluación y Rúbrica (Total: 5 Puntos)

| Criterio | Descripción | Puntos |
|---|---|:---:|
| **1. Extracción de Datos** | Calidad del scraper o cliente HTTP, modularidad, saneamiento de datos y manejo de errores de conexión. | 1.5 pts |
| **2. Persistencia en DB** | Estructura del esquema de base de datos, tipos correctos, unicidad y script reproducible de inicialización. | 1.0 pt |
| **3. API FastAPI y Pydantic** | Implementación completa de endpoints CRUD, validación estricta con Pydantic v2 y códigos de estado HTTP semánticos (200, 201, 400, 404). | 1.5 pts |
| **4. Documentación y Ejecución** | Claridad del README, fuentes de datos justificadas con el proyecto del foro y despliegue local sin fallos. | 1.0 pt |
| **Total** | | **5.0 pts** |
