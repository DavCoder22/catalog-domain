from src.models.search_model import SearchModel

class SearchService:
    @staticmethod
    def search_catalog(query, page=1, size=10):
        # Construir el cuerpo de la consulta con paginación
        body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["nombre", "descripcion", "material", "categoria"]
                }
            },
            "from": (page - 1) * size,
            "size": size
        }
        # Pasar el cuerpo de la consulta al modelo
        return SearchModel.search_catalog(body)

    @staticmethod
    def index_data(documents):
        return SearchModel.index_data(documents)
