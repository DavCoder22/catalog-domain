# catalog-domain/src/models/catalog_model.py
from pymongo import MongoClient
from config.dev_config import MONGO_URI
from bson import ObjectId

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
            return_document=True
        )
        return counter["value"]
