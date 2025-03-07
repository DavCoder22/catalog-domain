from pydantic import BaseModel
from neo4j import GraphDatabase
from config.dev_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

class Recommendation(BaseModel):
    id: str
    nombre: str
    precio: float

    class Config:
        from_attributes = True

class RecommendationModel:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def close(self):
        self.driver.close()

    def create_or_update_product(self, product_data):
        with self.driver.session() as session:
            session.write_transaction(self._create_or_update_product, product_data)

    @staticmethod
    def _create_or_update_product(tx, product_data):
        tx.run(
            """
            MERGE (p:Product {id: $id})
            SET p.nombre = $nombre,
                p.material = $material,
                p.precio = $precio,
                p.descripcion = $descripcion,
                p.imagen = $imagen,
                p.boquilla = $boquilla,
                p.densidadInfill = $densidadInfill,
                p.categoria = $categoria
            """,
            id=product_data["id"],
            nombre=product_data["nombre"],
            material=product_data["material"],
            precio=product_data["precio"],
            descripcion=product_data["descripcion"],
            imagen=product_data["imagen"],
            boquilla=product_data["boquilla"],
            densidadInfill=product_data["densidadInfill"],
            categoria=product_data["categoria"]
        )

    def establish_relationships(self, product_id, precio, categoria, material):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_similar_products, precio, categoria, material)
            for record in result:
                related_product_id = record["related_product_id"]
                session.write_transaction(self._create_relationship, product_id, related_product_id)

    @staticmethod
    def _find_similar_products(tx, precio, categoria, material):
        return tx.run(
            """
            MATCH (p:Product)
            WHERE p.precio = $precio AND p.categoria = $categoria AND p.material = $material
            RETURN p.id AS related_product_id
            LIMIT 5
            """,
            precio=precio, categoria=categoria, material=material
        )

    @staticmethod
    def _create_relationship(tx, product_id, related_product_id):
        tx.run(
            """
            MATCH (p:Product {id: $product_id}), (related:Product {id: $related_product_id})
            MERGE (p)-[:COMPRADO_JUNTO]->(related)
            """,
            product_id=product_id, related_product_id=related_product_id
        )
