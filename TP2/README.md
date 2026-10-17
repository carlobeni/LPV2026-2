# Trabajo Práctico 2 (TP2) — Bot de Inteligencia Artificial Accesible Mediante API Backend

## Requerimientos de Entrega

Para la entrega se requiere:
1. Creación de un Bot de Inteligencia Artificial accesible mediante API backend
2. Guardado de la información o historial en una base de datos
3. Disponibilización de la interacción con el bot a través de una API propia desarrollada en FastAPI (sin interfaz gráfica)

El dominio temático del bot de IA se definirá según el proyecto final elegido en el foro.

## Comentarios Adicionales

Para dotar de inteligencia al bot, la aplicación FastAPI debe integrarse con una **API base de modelos de lenguaje**, como la provista por **OpenAI** (o alternativas como Google Gemini, Anthropic Claude o Groq):
- Tu API en FastAPI funcionará como orquestador y backend intermedio: recibirá las consultas del cliente, gestionará la memoria de la conversación y consultará a la API base (ej. OpenAI) para generar las respuestas.
- Para este trabajo práctico **no se requiere interfaz gráfica de usuario**; la validación y pruebas se realizarán directamente mediante Swagger UI (`/docs`) o por terminal como cliente.
- El comportamiento y personalidad del bot deben calibrarse a través del *System Prompt* (instrucciones de sistema) para alinearse estrictamente al contexto temático de su proyecto final elegido en el foro:
- **Ejemplos de roles según el dominio del proyecto:**
  - **Analista Estadístico:** Si el proyecto trabaja con datos poblacionales, censos o métricas agregadas, el bot debe comportarse como un experto en análisis de datos, interpretando correlaciones, porcentajes y tendencias numéricas.
  - **Asistente Técnico Industrial:** Si el proyecto abarca telemetría mecatrónica, sensores o maquinaria, el bot debe adoptar el rol de un ingeniero de planta, utilizando terminología técnica precisa, sugiriendo rangos seguros de operación y pautas de mantenimiento preventivo.
  - **Consultor Especializado de Dominio:** Capaz de responder dudas puntuales sobre los registros almacenados en la base de datos poblada en el TP1.
- El bot debe mantener su personaje asignado de forma consistente y delimitar su alcance temático.

## Seguridad de Credenciales y Uso de `.env`

> [!WARNING]
> **Protección estricta de la API Key para evitar baneos:**
> - **Nunca incluyas tu API Key directamente en el código fuente ni la subas a GitHub.** Existen sistemas automáticos de escaneo (tanto de GitHub como de OpenAI) que detectan claves expuestas en repositorios públicos y proceden a **revocar y banear la API Key de forma inmediata**, dejando tu aplicación inutilizable y consumiendo saldo indebidamente.
> - Almacena las claves en un archivo local `.env`:
>   ```env
>   OPENAI_API_KEY=tu_clave_secreta_aqui
>   DATABASE_URL=sqlite:///./chat.db
>   ```
> - Asegúrate de que el archivo `.env` esté listado dentro de tu `.gitignore`.
> - Proporciona en el repositorio un archivo de muestra **`.env.example`** con las variables sin valores reales, para que el docente o evaluador pueda configurar su propia clave al momento de ejecutar:
>   ```env
>   OPENAI_API_KEY=
>   DATABASE_URL=sqlite:///./chat.db
>   ```
