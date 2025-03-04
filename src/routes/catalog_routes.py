# catalog-domain/src/routes/catalog_routes.py
from fastapi import APIRouter, HTTPException
from src.services.catalog_service import CatalogService
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class CatalogItem(BaseModel):
    nombre: str
    material: str
    precio: float
    descripcion: str
    imagen: str
    boquilla: str
    densidadInfill: int
    categoria: str
    opcionEnvio: Optional[str] = None
    colores: Optional[List[str]] = None

@router.get("/catalog", response_model=List[CatalogItem])
def get_all_catalogs():
    return CatalogService.get_all_catalogs()

@router.get("/catalog/{catalog_id}", response_model=CatalogItem)
def get_catalog_by_id(catalog_id: str):
    catalog = CatalogService.get_catalog_by_id(catalog_id)
    if catalog:
        return catalog
    raise HTTPException(status_code=404, detail="Catalog not found")

@router.post("/catalog", response_model=dict)
def add_catalog(catalog_data: CatalogItem):
    catalog_id = CatalogService.add_catalog(catalog_data.dict())
    return {"catalog_id": str(catalog_id)}

@router.put("/catalog/{catalog_id}", response_model=dict)
def update_catalog(catalog_id: str, updated_data: CatalogItem):
    result = CatalogService.update_catalog(catalog_id, updated_data.dict())
    if result.modified_count > 0:
        return {"message": "Catalog updated successfully"}
    raise HTTPException(status_code=404, detail="Catalog not found or no changes made")

@router.delete("/catalog/{catalog_id}", response_model=dict)
def delete_catalog(catalog_id: str):
    result = CatalogService.delete_catalog(catalog_id)
    if result.deleted_count > 0:
        return {"message": "Catalog deleted successfully"}
    raise HTTPException(status_code=404, detail="Catalog not found")
