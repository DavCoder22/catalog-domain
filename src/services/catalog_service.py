from src.models.catalog_model import CatalogModel
from src.models.search_model import SearchModel
from src.services.recommendation_service import RecommendationService

class CatalogService:
    @staticmethod
    def add_catalog(catalog_data):
        # Agregar el producto en MongoDB
        catalog_id = CatalogModel.add_catalog(catalog_data)

        # Preparar datos para Elasticsearch
        data = {
            "_id": str(catalog_id),
            "source": {
                "nombre": catalog_data["nombre"],
                "material": catalog_data["material"],
                "precio": catalog_data["precio"],
                "descripcion": catalog_data["descripcion"],
                "imagen": catalog_data["imagen"],
                "boquilla": catalog_data["boquilla"],
                "densidadInfill": catalog_data["densidadInfill"],
                "categoria": catalog_data["categoria"]
            }
        }
        SearchModel.index_data([data])

        # Crear nodo en Neo4j y establecer relaciones
        recommendation_service = RecommendationService()
        product_data = {
            "id": str(catalog_id),
            "nombre": catalog_data["nombre"],
            "material": catalog_data["material"],
            "precio": catalog_data["precio"],
            "descripcion": catalog_data["descripcion"],
            "imagen": catalog_data["imagen"],
            "boquilla": catalog_data["boquilla"],
            "densidadInfill": catalog_data["densidadInfill"],
            "categoria": catalog_data["categoria"]
        }
        recommendation_service.create_product_node(product_data)
        recommendation_service.establish_relationships(
            str(catalog_id),
            catalog_data["precio"],
            catalog_data["categoria"],
            catalog_data["material"]
        )

        return catalog_id

    @staticmethod
    def update_catalog(catalog_id, updated_data):
        # Actualizar el producto en MongoDB
        result = CatalogModel.update_catalog(catalog_id, updated_data)

        # Preparar datos para Elasticsearch
        data = {
            "_id": str(catalog_id),
            "source": {
                "nombre": updated_data.get("nombre", ""),
                "material": updated_data.get("material", ""),
                "precio": updated_data.get("precio", 0),
                "descripcion": updated_data.get("descripcion", ""),
                "imagen": updated_data.get("imagen", ""),
                "boquilla": updated_data.get("boquilla", ""),
                "densidadInfill": updated_data.get("densidadInfill", 0),
                "categoria": updated_data.get("categoria", "")
            }
        }
        SearchModel.index_data([data])

        # Actualizar nodo en Neo4j y relaciones
        recommendation_service = RecommendationService()
        product_data = {
            "id": str(catalog_id),
            "nombre": updated_data.get("nombre", ""),
            "material": updated_data.get("material", ""),
            "precio": updated_data.get("precio", 0),
            "descripcion": updated_data.get("descripcion", ""),
            "imagen": updated_data.get("imagen", ""),
            "boquilla": updated_data.get("boquilla", ""),
            "densidadInfill": updated_data.get("densidadInfill", 0),
            "categoria": updated_data.get("categoria", "")
        }
        recommendation_service.create_product_node(product_data)
        recommendation_service.establish_relationships(
            str(catalog_id),
            updated_data.get("precio", 0),
            updated_data.get("categoria", ""),
            updated_data.get("material", "")
        )

        return result

    @staticmethod
    def delete_catalog(catalog_id):
        # Eliminar el producto de MongoDB
        result = CatalogModel.delete_catalog(catalog_id)

        # Eliminar el producto de Elasticsearch
        SearchModel.es.delete(index="catalogosearch", id=catalog_id)

        # Eliminar el nodo de Neo4j
        recommendation_service = RecommendationService()
        recommendation_service.delete_product_node(catalog_id)

        return result
