from pymongo import MongoClient, ReturnDocument
from config.dev_config import MONGO_URI
from bson import ObjectId

# Conectar a la base de datos
client = MongoClient(MONGO_URI)
db = client.catalog_db
catalog_collection = db.catalog
counter_collection = db.counters

class CatalogModel:
    @staticmethod
    def get_all_catalogs():
        return list(catalog_collection.find())

    @staticmethod
    def get_catalog_by_id(catalog_id):
        return catalog_collection.find_one({"_id": ObjectId(catalog_id)})

    @staticmethod
    def add_catalog(catalog_data):
        # Verificar si la colección está vacía
        if catalog_collection.count_documents({}) == 0:
            # Reiniciar el contador si la colección está vacía
            counter_collection.update_one(
                {"_id": "order_number"},
                {"$set": {"value": 0}},
                upsert=True
            )

        # Obtener el siguiente número de pedido
        order_number = CatalogModel.get_next_order_number()
        catalog_data["idProducto"] = f"P{str(order_number).zfill(3)}"

        return catalog_collection.insert_one(catalog_data).inserted_id

    @staticmethod
    def update_catalog(catalog_id, updated_data):
        return catalog_collection.update_one({"_id": ObjectId(catalog_id)}, {"$set": updated_data})

    @staticmethod
    def delete_catalog(catalog_id):
        return catalog_collection.delete_one({"_id": ObjectId(catalog_id)})

    @staticmethod
    def get_next_order_number():
        # Incrementar y obtener el siguiente número de pedido
        counter = counter_collection.find_one_and_update(
            {"_id": "order_number"},
            {"$inc": {"value": 1}},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )
        return counter["value"]

    @staticmethod
    def reset_order_number():
        # Reiniciar el contador a 0
        counter_collection.update_one(
            {"_id": "order_number"},
            {"$set": {"value": 0}},
            upsert=True
        )
