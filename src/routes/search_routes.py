from fastapi import FastAPI
from src.controllers.search_controller import router as search_router

def create_app():
    app = FastAPI()
    # Incluir el router de búsqueda con el prefijo /api
    app.include_router(search_router, prefix="/api", tags=["search"])
    return app
