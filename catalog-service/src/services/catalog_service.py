from src.models.catalog_model import CatalogModel
from src.config.db_config import get_db_config

class CatalogService:
    def __init__(self):
        self.model = CatalogModel(get_db_config())

    def get_all_items(self):
        return self.model.get_all_items()

    def get_item_by_id(self, item_id):
        return self.model.get_item_by_id(item_id)

    def add_item(self, item):
        # Contar el número de artículos existentes
        current_count = self.model.count_items()
        # Generar el nuevo idProducto
        item['idProducto'] = f"P{str(current_count + 1).zfill(3)}"
        # Agregar el artículo con el nuevo idProducto
        return self.model.add_item(item)

    def update_item(self, item_id, updated_fields):
        return self.model.update_item(item_id, updated_fields)

    def delete_item(self, item_id):
        return self.model.delete_item(item_id)
