"""
Punto de entrada para el servidor ASGI Uvicorn.
"""
import uvicorn

if __name__ == "__main__":
    print("Iniciando servidor Uvicorn para FastAPI...")
    print("Documentación interactiva disponible en: http://127.0.0.1:8000/docs")
    uvicorn.run(
        "src.app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
