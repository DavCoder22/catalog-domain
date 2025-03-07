from elasticsearch import Elasticsearch, helpers
from config.dev_config import ELASTICSEARCH_HOSTS, ELASTICSEARCH_API_KEY

class SearchModel:
    es = Elasticsearch(
        hosts=ELASTICSEARCH_HOSTS,
        api_key=ELASTICSEARCH_API_KEY,
        verify_certs=True,
        ssl_show_warn=False
    )

    @staticmethod
    def search_catalog(body):
        index = "catalogosearch"
        query = {
            "query": {
                "multi_match": {
                    "query": body["query"],
                    "fields": ["nombre^2", "descripcion", "material", "categoria"]
                }
            },
            "from": (body["page"] - 1) * body["size"],
            "size": body["size"]
        }
        response = SearchModel.es.search(index=index, body=query)
        return response["hits"]["hits"]

    @staticmethod
    def index_data(documents):
        actions = [
            {
                "_index": doc["_index"],
                "_id": doc["_id"],
                "_source": doc["_source"]
            }
            for doc in documents if "_source" in doc
        ]
        helpers.bulk(SearchModel.es, actions)
