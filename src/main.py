#!/usr/bin/env python
"""Main entry point for the 3D Print Catalog Microservices API."""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
import uvicorn
import logging
from src.routes import catalog_routes, search_routes, recommendation_routes
from src.utils.helpers import get_config, connect_to_database
from src.utils.logging_config import setup_logging

# Configurar logging
setup_logging()
logger = logging.getLogger(__name__)

# Crear instancia de FastAPI
app = FastAPI(
    title="3D Print Catalog API",
    description="API for managing 3D printed products, including catalog, recommendations, and searches.",
    version="1.0.0",
    contact={
        "name": "Your Name",
        "email": "your.email@example.com",
    },
)

# Configurar CORS para permitir solicitudes desde el frontend (ajusta según necesidades)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar directorio estático para documentación (opcional)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Cargar configuración global
config = get_config(environment="dev")

# Incluir rutas
app.include_router(catalog_routes.router, prefix="/api/v1/catalog", tags=["catalog"])
app.include_router(search_routes.router, prefix="/api/v1/search", tags=["search"])
app.include_router(recommendation_routes.router, prefix="/api/v1/recommendations", tags=["recommendations"])

# Evento de inicio
@app.on_event("startup")
async def startup_event():
    """Initialize database connections and services on startup."""
    logger.info("Starting 3D Print Catalog API...")
    # Conectar a bases de datos (puedes inicializar aquí si es necesario)
    connect_to_database("mongodb", config)
    connect_to_database("neo4j", config)
    connect_to_database("elasticsearch", config)

# Evento de cierre
@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown."""
    logger.info("Shutting down 3D Print Catalog API...")

# Personalizar OpenAPI para Swagger UI
def custom_openapi():
    """Generate a custom OpenAPI schema for better documentation."""
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["info"]["contact"] = app.contact
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    # Ejecutar la aplicación con uvicorn para desarrollo
    logger.info("Running 3D Print Catalog API on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)