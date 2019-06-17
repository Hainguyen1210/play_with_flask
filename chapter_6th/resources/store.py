from flask_restful import Resource, reqparse, request
from flask_jwt import jwt_required
from models.store import StoreModel


class Store(Resource):
    # use parser to validate the input
    parser = reqparse.RequestParser()
    parser.add_argument('new_name', required=True, help='new name must be specified!')

    def get(self, name): 
        store = StoreModel.find_by_name(name)
        return (store.to_json(), 200) if store else ({'message': 'store not found'}, 404)
    
    @jwt_required()
    def post(self, name):
        # can't create 2 stores with the same name
        if StoreModel.find_by_name(name):
            return ({'messsage': 'A store with name "{}" alredy exists'.format(name)}, 400)
        
        store = StoreModel(name)
        store.save_to_db()
        return store.to_json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            if len(store.items.all()) == 0:
                store.delete()
                return ({'message': 'store has been deleted.'}, 200)
            else:
                return ({'message': 'cannot delete store that contains items.'}, 400)
        else:
            return ({'message': 'store not found.'}, 404)

    @jwt_required()
    def put(self, name):
        request_data = self.parser.parse_args()
        store = StoreModel.find_by_name(name)
        new_name = request_data.get('new_name')

        if store:
            store.name = new_name
            return_message = ({'message': 'store has been updated.'}, 200)
        else:
            store = StoreModel(name)
            return_message = ({'message': 'store has been added.'}, 201)

        store.save_to_db()
        return return_message


class StoreList(Resource):
    def get(self):

        return {'stores': list(map(lambda x: x.to_json_simple(request.host_url), StoreModel.query.all()))}
