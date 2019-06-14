from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
api = Api(app)
app.secret_key = 'jose'
jwt = JWT(app, authenticate, identity)

items = [ 
        {
            "name": "table",
            "price": 43
        },
        {
            "name": "car",
            "price": 200
        },
        {
            "name": "house",
            "price": 400
        }
    ]
class Item(Resource):
    # use parser to validate the input
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='this field cannot left blank!')

    def get(self, name): 
        item = next(filter(lambda x: x.get('name') == name, items), None)
        return (item, 200) if item else ({'item': None}, 404)
    
    # @jwt_required()
    def post(self, name):
        # can't create 2 items with the same name
        if next(filter(lambda x: x.get('name') == name, items), None):
            return ({'messsage': 'An item with name "{}" alredy exists'.format(name)}, 400)
        
        # request_data = request.get_json()
        request_data = self.parser.parse_args()

        item = {'name': name, 'price': request_data.get('price')}
        items.append(item)
        return item, 201
    
    # @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda x: x.get('name') != name, items))
        return ({'message': 'item has been deleted'}, 200)

    # @jwt_required()
    def put(self, name):
        # request_data = request.get_json()
        request_data = self.parser.parse_args()
        item = next(filter(lambda x: x.get('name') == name, items), None)
        if item:
            item.update(request_data)
            return ({'message': 'item has been updated'}, 200)
        else:
            items.append({'name': name, 'price': request_data.get('price')})
            return ({'message': 'item has been added'}, 200)


class ItemList(Resource): 
    def get(self): 
        return {'items': items}

api.add_resource(Item, '/items/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)