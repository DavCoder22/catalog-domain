from fastapi import APIRouter
from src.controllers.recommendation_controller import router as recommendation_router

app = APIRouter()
app.include_router(recommendation_router, prefix="/api", tags=["recommendations"])
