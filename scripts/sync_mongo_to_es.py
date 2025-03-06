# catalog-domain/src/scripts/sync_mongo_to_es.py
from src.models.catalog_model import CatalogModel
from src.models.search_model import SearchModel

def sync_mongo_to_es():
    # Obtener todos los documentos de MongoDB
    catalogs = CatalogModel.get_all_catalogs()

    # Preparar los documentos para Elasticsearch
    documents = []
    for catalog in catalogs:
        doc = {
            "index": {"_index": "catalogosearch", "_id": str(catalog["_id"])}
        }
        data = {
            "nombre": catalog["nombre"],
            "material": catalog["material"],
            "precio": catalog["precio"],
            "descripcion": catalog["descripcion"],
            "imagen": catalog["imagen"],
            "boquilla": catalog["boquilla"],
            "densidadInfill": catalog["densidadInfill"],
            "categoria": catalog["categoria"]
        }
        documents.append(doc)
        documents.append(data)

    # Indexar los documentos en Elasticsearch
    SearchModel.index_data(documents)

if __name__ == "__main__":
    sync_mongo_to_es()
