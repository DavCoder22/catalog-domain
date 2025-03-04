# catalog-domain/src/controllers/catalog_controller.py
from flask import Blueprint, jsonify, request
from flask_cors import CORS
from src.services.catalog_service import CatalogService

catalog_blueprint = Blueprint('catalog', __name__)
CORS(catalog_blueprint)  # Habilitar CORS para este blueprint

@catalog_blueprint.route('/catalog', methods=['GET'])
def get_all_catalogs():
    catalogs = CatalogService.get_all_catalogs()
    return jsonify(catalogs), 200

@catalog_blueprint.route('/catalog/<catalog_id>', methods=['GET'])
def get_catalog_by_id(catalog_id):
    catalog = CatalogService.get_catalog_by_id(catalog_id)
    if catalog:
        return jsonify(catalog), 200
    return jsonify({"error": "Catalog not found"}), 404

@catalog_blueprint.route('/catalog', methods=['POST'])
def add_catalog():
    catalog_data = request.json
    catalog_id = CatalogService.add_catalog(catalog_data)
    return jsonify({"catalog_id": str(catalog_id)}), 201

@catalog_blueprint.route('/catalog/<catalog_id>', methods=['PUT'])
def update_catalog(catalog_id):
    updated_data = request.json
    result = CatalogService.update_catalog(catalog_id, updated_data)
    if result.modified_count > 0:
        return jsonify({"message": "Catalog updated successfully"}), 200
    return jsonify({"error": "Catalog not found or no changes made"}), 404

@catalog_blueprint.route('/catalog/<catalog_id>', methods=['DELETE'])
def delete_catalog(catalog_id):
    result = CatalogService.delete_catalog(catalog_id)
    if result.deleted_count > 0:
        return jsonify({"message": "Catalog deleted successfully"}), 200
    return jsonify({"error": "Catalog not found"}), 404
