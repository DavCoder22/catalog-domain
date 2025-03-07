from fastapi import APIRouter, HTTPException, Query
from src.services.search_service import SearchService

router = APIRouter()

@router.get("/search")
def search_catalog(query: str = Query(..., min_length=1), page: int = Query(1, ge=1), size: int = Query(10, ge=1)):
    try:
        body = {"query": query, "page": page, "size": size}
        results = SearchService.search_catalog(body)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
