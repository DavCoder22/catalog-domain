from pymongo import MongoClient
from bson import ObjectId

class CatalogModel:
    def __init__(self, db_config):
        self.client = MongoClient(db_config['mongo_uri'])
        self.db = self.client[db_config['database_name']]
        self.collection = self.db['catalog']

    def get_all_items(self):
        items = list(self.collection.find())
        for item in items:
            item['_id'] = str(item['_id'])
        return items

    def get_item_by_id(self, item_id):
        item = self.collection.find_one({'_id': ObjectId(item_id)})
        if item:
            item['_id'] = str(item['_id'])
        return item

    def add_item(self, item):
        result = self.collection.insert_one(item)
        return str(result.inserted_id)

    def update_item(self, item_id, updated_fields):
        result = self.collection.update_one({'_id': ObjectId(item_id)}, {'$set': updated_fields})
        return result.matched_count > 0

    def delete_item(self, item_id):
        result = self.collection.delete_one({'_id': ObjectId(item_id)})
        return result.deleted_count > 0

    def count_items(self):
        return self.collection.count_documents({})
