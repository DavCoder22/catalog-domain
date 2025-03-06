# catalog-domain/src/routes/search_routes.py
from fastapi import FastAPI
from src.controllers.search_controller import router as search_router

def create_app():
    app = FastAPI()
    app.include_router(search_router, prefix="/api")
    return app
