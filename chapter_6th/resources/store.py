from flask_jwt import jwt_required
from flask_restful import Resource, reqparse, inputs

from models.store import StoreModel
from my_utils import make_response_message


class Store(Resource):
    put_parser = reqparse.RequestParser()
    put_parser.add_argument(
        'new_name', type=inputs.regex('^.{,80}$'), required=True,
        help='Must be less than 80 characters', trim=True)

    @staticmethod
    def response_not_found(store_id):
        return make_response_message('Store id:{} not found'.format(store_id), 404)

    def get(self, store_id):
        store = StoreModel.find_by_id(store_id)
        if not store:
            return self.__class__.response_not_found(store_id)
        return store.to_json_with_items(), 200

    @jwt_required()
    def delete(self, store_id):
        store = StoreModel.find_by_id(store_id)
        if not store:
            return self.__class__.response_not_found(store_id)

        if len(store.items.all()) > 0:
            return make_response_message('Cannot delete store that contains items', 400)

        store.delete()
        return make_response_message("Store '{}' deleted".format(store_id), 200)

    @jwt_required()
    def put(self, store_id):
        new_name = self.put_parser.parse_args()['new_name']
        store = StoreModel.find_by_id(store_id)

        if not store:
            return self.__class__.response_not_found(store_id)

        store.name = new_name
        store.save_to_db()
        return make_response_message('Store updated', 200)


class Stores(Resource):
    post_parser = reqparse.RequestParser()
    post_parser.add_argument(
        'name', type=inputs.regex('^.{,80}$'), required=True,
        help='Must be less than 80 characters', trim=True)

    @staticmethod
    def get():
        return [store.to_json_simple() for store in StoreModel.query.all()]

    @jwt_required()
    def post(self):
        store = StoreModel(self.post_parser.parse_args()['name'])
        store.save_to_db()
        return store.to_json_simple(), 201
