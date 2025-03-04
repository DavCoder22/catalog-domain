# catalog-domain/scripts/init_db_script.py
from pymongo import MongoClient
from config.dev_config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client.catalog_db
catalog_collection = db.catalog

def init_db():
    # Insertar datos de ejemplo o crear índices
    catalog_collection.insert_many([
        {"name": "Catalog 1", "description": "Description 1"},
        {"name": "Catalog 2", "description": "Description 2"}
    ])

if __name__ == "__main__":
    init_db()
