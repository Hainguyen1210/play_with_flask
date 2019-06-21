from flask_jwt import jwt_required
from flask_restful import Resource, reqparse, inputs

from models.item import ItemModel
from models.store import StoreModel
from my_utils import make_response_message
from resources.store import Store


class Item(Resource):
    # Use parser to validate the input
    put_parser = reqparse.RequestParser()
    put_parser.add_argument(
        'new_name', type=inputs.regex('^.{,80}$'),
        help="Must be less than 80 characters", trim=True)
    put_parser.add_argument(
        'new_price', type=inputs.positive,
        help="Must be positive")
    put_parser.add_argument('new_store_id', type=int)

    @staticmethod
    def response_not_found(item_id):
        return make_response_message('Item id:{} not found'.format(item_id), 404)

    def get(self, store_id, item_id):
        # Validate current store_id
        current_store = StoreModel.find_by_id(store_id)
        if not current_store:
            return Store.response_not_found(store_id)

        item = current_store.find_item(item_id)
        if not item:
            return self.__class__.response_not_found(item_id)
        return item.to_json(), 200

    @jwt_required()
    def delete(self, store_id, item_id):
        # Validate current store_id
        if not StoreModel.find_by_id(store_id):
            return Store.response_not_found(store_id)

        item = ItemModel.find_by_id(item_id)
        if not item:
            return self.__class__.response_not_found(item_id)
        item.delete()
        return make_response_message("Item '{}' deleted".format(item_id), 200)

    @jwt_required()
    def put(self, store_id, item_id):
        # Validate current store_id
        current_store = StoreModel.find_by_id(store_id)
        if not current_store:
            return Store.response_not_found(store_id)

        request_data = self.put_parser.parse_args()
        new_name = request_data.get('new_name')
        new_price = request_data.get('new_price')
        new_store_id = request_data.get('new_store_id')

        if not (new_name or new_store_id or new_price):
            return make_response_message('Nothing to update', 400)

        # Validate new store_id
        if new_store_id:
            new_store = StoreModel.find_by_id(new_store_id)
            if not new_store:
                return Store.response_not_found(new_store_id)

        # Validate item
        item = current_store.find_item(item_id)
        if not item:
            return self.__class__.response_not_found(item_id)

        item.name = new_name if new_name else item.name
        item.price = new_price if new_price else item.price
        item.store_id = new_store_id if new_store_id else item.store_id
        item.save_to_db()

        return make_response_message('Item updated', 200)


class Items(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument(
        'name', type=inputs.regex('^.{,80}$'), required=True,
        help="Must be less than 80 characters", trim=True)
    post_parser.add_argument(
        'price', type=inputs.positive, required=True,
        help="Must be positive")

    def get(self, store_id):
        # Validate store_id
        store = StoreModel.find_by_id(store_id)
        if not store:
            return Store.response_not_found(store_id)

        return [item.to_json() for item in store.items]

    @jwt_required()
    def post(self, store_id):
        # Validate store_id
        store = StoreModel.find_by_id(store_id)
        if not store:
            return Store.response_not_found(store_id)

        request_data = self.post_parser.parse_args()
        item = ItemModel(request_data['name'], request_data['price'], store_id)
        item.save_to_db()
        return item.to_json(), 201


class AllItems(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument(
        'name', type=inputs.regex('^.{,80}$'), required=True,
        help="Must be less than 80 characters", trim=True)

    def get(self):
        return [item.to_json() for item in ItemModel.query.all()]
