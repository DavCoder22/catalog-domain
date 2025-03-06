# catalog-domain/src/services/catalog_service.py
from src.models.catalog_model import CatalogModel
from src.models.search_model import SearchModel

class CatalogService:
    @staticmethod
    def get_all_catalogs():
        return CatalogModel.get_all_catalogs()

    @staticmethod
    def get_catalog_by_id(catalog_id):
        return CatalogModel.get_catalog_by_id(catalog_id)

    @staticmethod
    def add_catalog(catalog_data):
        # Agregar el producto en MongoDB
        catalog_id = CatalogModel.add_catalog(catalog_data)

        # Indexar el nuevo producto en Elasticsearch
        doc = {
            "index": {"_index": "catalogosearch", "_id": str(catalog_id)}
        }
        data = {
            "nombre": catalog_data["nombre"],
            "material": catalog_data["material"],
            "precio": catalog_data["precio"],
            "descripcion": catalog_data["descripcion"],
            "imagen": catalog_data["imagen"],
            "boquilla": catalog_data["boquilla"],
            "densidadInfill": catalog_data["densidadInfill"],
            "categoria": catalog_data["categoria"]
        }
        SearchModel.index_data([doc, data])

        return catalog_id

    @staticmethod
    def update_catalog(catalog_id, updated_data):
        # Actualizar el producto en MongoDB
        result = CatalogModel.update_catalog(catalog_id, updated_data)

        # Actualizar el producto en Elasticsearch
        doc = {
            "index": {"_index": "catalogosearch", "_id": str(catalog_id)}
        }
        data = {
            "nombre": updated_data["nombre"],
            "material": updated_data["material"],
            "precio": updated_data["precio"],
            "descripcion": updated_data["descripcion"],
            "imagen": updated_data["imagen"],
            "boquilla": updated_data["boquilla"],
            "densidadInfill": updated_data["densidadInfill"],
            "categoria": updated_data["categoria"]
        }
        SearchModel.index_data([doc, data])

        return result

    @staticmethod
    def delete_catalog(catalog_id):
        # Eliminar el producto de MongoDB
        result = CatalogModel.delete_catalog(catalog_id)

        # Eliminar el producto de Elasticsearch
        SearchModel.es.delete(index="catalogosearch", id=catalog_id)

        return result
