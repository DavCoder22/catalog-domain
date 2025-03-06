# catalog-domain/src/controllers/search_controller.py
from fastapi import APIRouter, HTTPException, Query
from src.services.search_service import SearchService
from pydantic import BaseModel
from typing import List

router = APIRouter()

class SearchQuery(BaseModel):
    query: str

class IndexDocument(BaseModel):
    index: dict
    data: dict

@router.get("/search")
def search_catalog(query: str, page: int = Query(1, ge=1), size: int = Query(10, ge=1)):
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["nombre", "descripcion", "material", "categoria"]
            }
        },
        "from": (page - 1) * size,
        "size": size
    }
    results = SearchService.search_catalog(body)
    if not results:
        raise HTTPException(status_code=404, detail="No results found")
    return results

@router.post("/index")
def index_data(documents: List[IndexDocument]):
    # Correctly format the documents for bulk indexing
    formatted_documents = [
        item for doc in documents for item in (doc.index, doc.data)
    ]
    response = SearchService.index_data(formatted_documents)
    return {"status": "success", "response": response}
