# Trabajo Práctico 2 (TP2) — Bot de Inteligencia Artificial Accesible Mediante API Backend

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
| **Periodo de Desarrollo** | Semanas 5 hasta el día del 1er Parcial (Semana 7) |
| **Fecha Límite de Entrega** | Día del 1er Parcial |
| **Modalidad** | Grupal (mismo equipo del TP1 y proyecto final) |
| **Interfaz Gráfica** | **Sin interfaz gráfica requerida** (interacción exclusiva vía API backend) |

---

## Requerimientos de Entrega

Para la entrega se requiere:
1. Creación de un Bot de Inteligencia Artificial accesible mediante API backend
2. Integración de lógica de inferencia, procesamiento de lenguaje natural o agentes inteligentes (vía LLMs, APIs de IA, o modelos locales)
3. Persistencia de contexto, conversaciones o base de conocimiento en una base de datos
4. Disponibilización e interacción con el bot a través de una API propia desarrollada en FastAPI (sin interfaz gráfica obligatoria)

El dominio temático del bot de IA se definirá según el proyecto final elegido en el foro.

---

## 1. Alcance Técnico y Especificaciones

### 1.1 Núcleo de Inteligencia Artificial
- **Mecanismos de IA Aceptados:**
  - **Modelos de Lenguaje por API (LLMs):** Integración con OpenAI (GPT-4o / GPT-3.5), Google Gemini API, Anthropic Claude, Groq o Mistral API.
  - **Modelos Locales / Auto-alojados:** Ejecución local mediante Ollama (Llama 3, Mistral, Phi-3) o modelos de HuggingFace Transformers.
  - **Agentes Inteligentes y RAG (Retrieval-Augmented Generation):** Búsqueda semántica sobre la base de datos poblada en el TP1 o documentos de dominio del proyecto.
  - **Sistemas Expertos / Clasificadores NLP:** Modelos de procesamiento de texto con scikit-learn, SpaCy o redes neuronales para clasificación/predicción técnica.
- **Configuración del Agente:**
  - *System Prompt* robusto que delimite la personalidad, contexto operativo y restricciones de seguridad del bot acorde al tema del foro.
  - Manejo de parámetros de inferencia (`temperature`, `max_tokens`, `top_p`).

### 1.2 Persistencia de Memoria y Contexto
- **Gestión de Sesiones:**
  - Identificación por `session_id` o `usuario_id` para permitir múltiples conversaciones simultáneas independientes.
- **Almacenamiento en Base de Datos (SQLite / PostgreSQL):**
  - Tabla de conversaciones o mensajes (`id`, `session_id`, `rol: user|assistant|system`, `mensaje`, `timestamp`).
  - Recuperación de los últimos *N* mensajes para proporcionar memoria de corto plazo al modelo en cada turno conversacional.

### 1.3 Disponibilización mediante API FastAPI (Sin Frontend Requerido)
- **Framework:** `FastAPI` con tipado riguroso mediante `Pydantic v2`.
- **Endpoints Mínimos Requeridos:**
  - `POST /api/chat`: Recepción del mensaje del usuario y generación de la respuesta del bot.
    - Entrada: `{"session_id": "...", "mensaje": "..."}`
    - Salida: `{"session_id": "...", "respuesta": "...", "tokens_usados": 120, "timestamp": "..."}`
  - `GET /api/chat/{session_id}/historial`: Consulta del historial completo de una sesión específica.
  - `DELETE /api/chat/{session_id}`: Reseteo de memoria o borrado de una conversación.
  - `GET /api/estado`: Endpoint de monitoreo que verifique la conectividad con el proveedor de IA o modelo local.
- **Pruebas y Documentación:**
  - Toda la interacción, validación y prueba funcional se realiza a través de **Swagger UI** (`http://localhost:8000/docs`), Postman o comandos `curl`.

---

## 2. Estructura de Proyecto Recomendada

```
tp2-bot-ia/
├── bot/
│   ├── __init__.py
│   ├── ai_client.py         <- Conexión con el proveedor LLM (Gemini, OpenAI, Ollama)
│   ├── prompts.py           <- Prompts de sistema y directivas del dominio
│   └── memory.py            <- Lógica de armado de ventana de contexto
├── database/
│   ├── __init__.py
│   ├── connection.py        <- Conexión a la base de datos (SQLite / PostgreSQL)
│   └── models.py            <- Tablas de sesiones y mensajes
├── routers/
│   ├── __init__.py
│   └── chat.py              <- Rutas y controladores de FastAPI
├── main.py                  <- Punto de entrada de la aplicación FastAPI
├── schemas.py               <- Esquemas Pydantic v2 (ChatRequest, ChatResponse, etc.)
├── .env.example             <- Plantilla de variables de entorno (API Keys seguras)
├── pyproject.toml / req.txt <- Dependencias
└── README.md                <- Documentación técnica del bot y guía de inicio
```

---

## 3. Seguridad y Variables de Entorno

> [!WARNING]
> **Protección de Credenciales:** Nunca incluyas claves de API (`OPENAI_API_KEY`, `GEMINI_API_KEY`) en el código fuente ni en el historial de Git. Emplea siempre un archivo `.env` agregado a tu `.gitignore` y proporciona un archivo `.env.example` con variables vacías para evaluación.

---

## 4. Instrucciones de Ejecución

1. Configurar el entorno virtual e instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Configurar la clave de API en el archivo `.env`:
   ```bash
   cp .env.example .env
   # Editar .env y colocar la API Key correspondiente
   ```
3. Iniciar el servicio con Uvicorn:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
4. Probar la API en la consola interactiva:
   👉 **`http://localhost:8000/docs`**

---

## 5. Criterios de Evaluación y Rúbrica (Total: 5 Puntos)

| Criterio | Descripción | Puntos |
|---|---|:---:|
| **1. Núcleo de Inteligencia Artificial** | Calidad de la integración con el modelo/LLM, adecuación del *system prompt* al dominio del proyecto y coherencia de las respuestas. | 1.5 pts |
| **2. Persistencia y Memoria de Contexto** | Almacenamiento correcto de sesiones e historial en base de datos, permitiendo conversaciones fluidas con memoria de turnos previos. | 1.5 pts |
| **3. Arquitectura API FastAPI & Pydantic** | Endpoints de chat e historial bien diseñados, validaciones de esquema con Pydantic v2 y códigos de estado semánticos. | 1.0 pt |
| **4. Seguridad y Documentación** | Manejo adecuado de variables de entorno (.env), Swagger interactivo operativo y README claro con ejemplos de payloads. | 1.0 pt |
| **Total** | | **5.0 pts** |
