"""
Inicialización de la aplicación FastAPI.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import API_TITLE, API_DESCRIPTION, API_VERSION
from src.routes import router as sensores_router


def create_app() -> FastAPI:
    app = FastAPI(
        title=API_TITLE,
        description=API_DESCRIPTION,
        version=API_VERSION,
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # Configuración de CORS para permitir consumo desde frontends visuales
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Endpoint de verificación de salud y bienvenida
    @app.get("/", tags=["Sistema"])
    def root():
        return {
            "mensaje": "Bienvenido a la API de Monitoreo Mecatrónico",
            "version": API_VERSION,
            "documentacion_swagger": "/docs",
            "documentacion_redoc": "/redoc",
            "estado": "operativo"
        }

    # Registrar enrutadores de recursos
    app.include_router(sensores_router)

    return app


app = create_app()
