import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required



class Item(Resource):
    # use parser to validate the input
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='this field cannot left blank!')

    @classmethod
    def find_by_name(cls, item_name):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query = "SELECT * FROM items WHERE name=?"
        results = cur.execute(query, (item_name, ))
        row = results.fetchone()
        if row:
            item = {
                    'name': row[1], 
                    'price': row[2]
                }
        else:
            item = {}
        con.close()
        return item

    def get(self, name): 
        item = self.find_by_name(name)
        return (item, 200) if item else ({'message': 'item not found'}, 404)
    
    # @jwt_required()
    def post(self, name):
        # can't create 2 items with the same name
        if self.find_by_name(name): 
            return ({'messsage': 'An item with name "{}" alredy exists'.format(name)}, 400)
        
        # request_data = request.get_json()
        request_data = self.parser.parse_args()
        item = (name, request_data.get('price'))

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        insert_query = "INSERT INTO items (name, price) VALUES (?, ?);"
        cursor.execute(insert_query, item)
        connection.commit()
        connection.close()

        item = {'name': name, 'price': request_data.get('price')}
        return item, 201
    
    # @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        delete_query = "DELETE FROM items WHERE name=?;"
        cursor.execute(delete_query, (name,))
        connection.commit()
        connection.close()
        
        return ({'message': 'item has been deleted'}, 200)

    # @jwt_required()
    def put(self, name):
        # request_data = request.get_json()
        request_data = self.parser.parse_args()
        item = self.find_by_name(name)

        # setup connections
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        if item:
            update_query = "UPDATE items SET price=? WHERE name=?;"
            cursor.execute(update_query, (request_data.get('price'), name))
            return_message = ({'message': 'item has been updated'}, 200)
        else:
            item = (name, request_data.get('price'))
            insert_query = "INSERT INTO items (name, price) VALUES (?, ?);"
            cursor.execute(insert_query, item)
            
            return_message = ({'message': 'item has been added'}, 200)

        connection.commit()
        connection.close()
        return return_message


class ItemList(Resource): 
    def get(self): 

        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query = "SELECT * FROM items"
        results = cur.execute(query)
        items = []
        for row in results: 
            item = {
                    'name': row[1], 
                    'price': row[2]
                }
            items.append(item)
        con.close()
        return {'items': items}