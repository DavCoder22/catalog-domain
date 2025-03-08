from flask import Blueprint, jsonify, request
from src.services.catalog_service import CatalogService

catalog_routes = Blueprint('catalog', __name__)
catalog_service = CatalogService()

@catalog_routes.route('/items', methods=['GET'])
def get_items():
    items = catalog_service.get_all_items()
    return jsonify(items), 200

@catalog_routes.route('/items/<item_id>', methods=['GET'])
def get_item(item_id):
    item = catalog_service.get_item_by_id(item_id)
    if item:
        return jsonify(item), 200
    return jsonify({'error': 'Item not found'}), 404

@catalog_routes.route('/items', methods=['POST'])
def add_item():
    item = request.json
    item_id = catalog_service.add_item(item)
    return jsonify({'message': 'Item added', 'id': item_id}), 201

@catalog_routes.route('/items/<item_id>', methods=['PUT'])
def update_item(item_id):
    updated_fields = request.json
    success = catalog_service.update_item(item_id, updated_fields)
    if success:
        return jsonify({'message': 'Item updated'}), 200
    return jsonify({'error': 'Item not found'}), 404

@catalog_routes.route('/items/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    success = catalog_service.delete_item(item_id)
    if success:
        return jsonify({'message': 'Item deleted'}), 200
    return jsonify({'error': 'Item not found'}), 404
