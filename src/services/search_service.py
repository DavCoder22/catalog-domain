from src.models.search_model import SearchModel

class SearchService:
    @staticmethod
    def search_catalog(body):
        return SearchModel.search_catalog(body)
