from src.models.recommendation_model import RecommendationModel

class RecommendationService:
    def __init__(self):
        self.model = RecommendationModel()

    def get_recommendations(self, product_id, limit=5):
        with self.model.driver.session() as session:
            result = session.run(
                """
                MATCH (p:Product {id: $product_id})-[:COMPRADO_JUNTO]->(rec:Product)
                RETURN rec.id AS id, rec.nombre AS nombre, rec.precio AS precio
                LIMIT $limit
                """,
                product_id=product_id, limit=limit
            )
            recommendations = [
                {"id": record["id"], "nombre": record["nombre"], "precio": record["precio"]}
                for record in result
            ]
            return recommendations
