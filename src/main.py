from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.catalog_routes import router as catalog_router
from src.routes.search_routes import create_app
from src.controllers.recommendation_controller import router as recommendation_router
from scripts.sync_mongo_to_es import sync_mongo_to_es  # Importación correcta

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los routers adicionales
app.include_router(catalog_router, prefix="/api")
app.include_router(recommendation_router, prefix="/api", tags=["recommendations"])

@app.on_event("startup")
async def startup_event():
    sync_mongo_to_es()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
