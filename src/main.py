# catalog-domain/src/main.py
from src.routes.catalog_routes import router as catalog_router
from src.routes.search_routes import create_app
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = create_app()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los routers
app.include_router(catalog_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
