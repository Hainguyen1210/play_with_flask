import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    # use parser to validate the input
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='this field cannot left blank!')

    def get(self, name): 
        item = ItemModel.find_by_name(name)
        return (item.to_json(), 200) if item else ({'message': 'item not found'}, 404)
    
    @jwt_required()
    def post(self, name):
        # can't create 2 items with the same name
        if ItemModel.find_by_name(name): 
            return ({'messsage': 'An item with name "{}" alredy exists'.format(name)}, 400)
        
        request_data = self.parser.parse_args()
        item = ItemModel(name, request_data.get('price'))
        item.save_to_db()
        return item.to_json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete()
            return ({'message': 'item has been deleted'}, 200)
        else:
            return ({'message': 'item not found'}, 404)

    @jwt_required()
    def put(self, name):
        request_data = self.parser.parse_args()
        price = request_data.get('price')
        item = ItemModel.find_by_name(name)

        if item:
            item.price = price
            return_message = ({'message': 'item has been updated'}, 200)
        else:
            item = ItemModel(name, price)
            return_message = ({'message': 'item has been added'}, 200)

        item.save_to_db()
        return return_message


class ItemList(Resource):
    def get(self):

        return {'items': list(map(lambda x: x.to_json(), ItemModel.query.all()))}
