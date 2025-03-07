import requests
from src.models.catalog_model import CatalogModel
from src.models.search_model import SearchModel

GRAPHQL_URL = "http://localhost:4000/graphql"  # URL del servidor GraphQL

def sync_mongo_to_es():
    # Obtener todos los documentos de MongoDB
    catalogs = CatalogModel.get_all_catalogs()

    # Preparar los documentos para Elasticsearch
    es_documents = []
    neo4j_data = []

    for catalog in catalogs:
        if all(key in catalog for key in ("nombre", "material", "precio", "descripcion", "imagen", "boquilla", "densidadInfill", "categoria")):
            es_doc = {
                "_index": "catalogosearch",
                "_id": str(catalog["_id"]),
                "_source": {
                    "nombre": catalog["nombre"],
                    "material": catalog["material"],
                    "precio": catalog["precio"],
                    "descripcion": catalog["descripcion"],
                    "imagen": catalog["imagen"],
                    "boquilla": catalog["boquilla"],
                    "densidadInfill": catalog["densidadInfill"],
                    "categoria": catalog["categoria"]
                }
            }
            es_documents.append(es_doc)

            neo4j_data.append({
                "id": str(catalog["_id"]),
                "nombre": catalog["nombre"],
                "material": catalog["material"],
                "precio": catalog["precio"],
                "descripcion": catalog["descripcion"],
                "imagen": catalog["imagen"],
                "boquilla": catalog["boquilla"],
                "densidadInfill": catalog["densidadInfill"],
                "categoria": catalog["categoria"]
            })

    # Indexar los documentos en Elasticsearch
    SearchModel.index_data(es_documents)

    # Sincronizar con Neo4j a través de GraphQL
    for data in neo4j_data:
        query = """
        mutation($id: ID!, $nombre: String!, $material: String!, $precio: Float!, $descripcion: String!, $imagen: String!, $boquilla: String!, $densidadInfill: String!, $categoria: String!) {
          createProduct(id: $id, nombre: $nombre, material: $material, precio: $precio, descripcion: $descripcion, imagen: $imagen, boquilla: $boquilla, densidadInfill: $densidadInfill, categoria: $categoria) {
            id
          }
        }
        """
        variables = {
            "id": data["id"],
            "nombre": data["nombre"],
            "material": data["material"],
            "precio": data["precio"],
            "descripcion": data["descripcion"],
            "imagen": data["imagen"],
            "boquilla": data["boquilla"],
            "densidadInfill": data["densidadInfill"],
            "categoria": data["categoria"]
        }
        response = requests.post(GRAPHQL_URL, json={'query': query, 'variables': variables})
        if response.status_code == 200:
            print(f"Product {data['id']} synchronized successfully.")
        else:
            print(f"Failed to synchronize product {data['id']}: {response.text}")

if __name__ == "__main__":
    sync_mongo_to_es()
