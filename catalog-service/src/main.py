from flask import Flask
from flask_cors import CORS
from src.routes.catalog_routes import catalog_routes

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

app.register_blueprint(catalog_routes, url_prefix='/api/catalog')

if __name__ == '__main__':
    app.run(debug=True)
