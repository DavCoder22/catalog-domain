# catalog-domain/src/services/catalog_service.py
from src.models.catalog_model import CatalogModel

class CatalogService:
    @staticmethod
    def get_all_catalogs():
        return CatalogModel.get_all_catalogs()

    @staticmethod
    def get_catalog_by_id(catalog_id):
        return CatalogModel.get_catalog_by_id(catalog_id)

    @staticmethod
    def add_catalog(catalog_data):
        # El modelo se encargará de generar el idProducto
        return CatalogModel.add_catalog(catalog_data)

    @staticmethod
    def update_catalog(catalog_id, updated_data):
        return CatalogModel.update_catalog(catalog_id, updated_data)

    @staticmethod
    def delete_catalog(catalog_id):
        return CatalogModel.delete_catalog(catalog_id)
