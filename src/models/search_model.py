from elasticsearch import Elasticsearch
from config.dev_config import ELASTICSEARCH_HOSTS, ELASTICSEARCH_API_KEY

# Inicializar el cliente de Elasticsearch
es = Elasticsearch(
    [ELASTICSEARCH_HOSTS],
    api_key=ELASTICSEARCH_API_KEY,
    verify_certs=True,
    ssl_show_warn=False
)

class SearchModel:
    es = es  # Asignar el cliente de Elasticsearch como un atributo de clase

    @staticmethod
    def search_catalog(body):
        index = "catalogosearch"
        response = SearchModel.es.search(index=index, body=body)
        return response["hits"]["hits"]

    @staticmethod
    def index_data(documents):
        response = SearchModel.es.bulk(operations=documents, pipeline="ent-search-generic-ingestion")
        return response

    @staticmethod
    def delete_catalog(catalog_id):
        index = "catalogosearch"
        response = SearchModel.es.delete(index=index, id=catalog_id)
        return response
