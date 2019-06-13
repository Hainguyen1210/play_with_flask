from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
api = Api(app)
app.secret_key = 'jose'
jwt = JWT(app, authenticate, identity)

items = []

class Item(Resource):
    def get(self, name): 
        item = next(filter(lambda x: x.get('name') == name, items), None)
        return (item, 200) if item else ({'item': None}, 404)
    
    @jwt_required()
    def post(self, name):
        if next(filter(lambda x: x.get('name') == name, items), None):
            return ({'messsage': 'An item with name "{}" alredy exists'.format(name)}, 400)

        request_data = request.get_json()
        item = {'name': name, 'price': request_data.get('price')}
        items.append(item)
        return item, 201

class ItemList(Resource): 
    def get(self): 
        return {'items': items}

api.add_resource(Item, '/items/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)