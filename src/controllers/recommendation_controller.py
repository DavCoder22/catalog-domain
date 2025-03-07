from fastapi import APIRouter, HTTPException
from src.services.recommendation_service import RecommendationService
from src.models.recommendation_model import Recommendation

router = APIRouter()
recommendation_service = RecommendationService()

@router.get("/recommendations/{product_id}", response_model=list[Recommendation])
def get_recommendations(product_id: str, limit: int = 5):
    try:
        recommendations = recommendation_service.get_recommendations(product_id, limit)
        if not recommendations:
            raise HTTPException(status_code=404, detail="No recommendations found")
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
