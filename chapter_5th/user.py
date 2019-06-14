import sqlite3
from flask_restful import Resource, reqparse

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query = "SELECT * FROM users WHERE username=?"
        results = cur.execute(query, (username, ))
        row = results.fetchone()
        if row:
            user = cls(*row)
        else:
            user =  None
        
        con.close()
        return user

    @classmethod
    def find_by_id(cls, id):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query = "SELECT * FROM users WHERE id=?"
        results = cur.execute(query, (id, ))
        row = results.fetchone()
        if row:
            user = cls(*row)
        else:
            user =  None
        
        con.close()
        return user

class UserRegister(Resource):
    # use parser to validate the input
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='username cannot be blank!')
    parser.add_argument('password', type=str, required=True, help='password cannot be blank!')

    def post(self):
        request_data = self.parser.parse_args()
        username = request_data.get('username')
        password = request_data.get('password')

        # check if the username exists
        if User.find_by_username(username):
            return ({'messsage': 'user name "{}" alredy exists'.format(username)}, 400)


        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        user = (username, password)
        insert_query = "INSERT INTO users (username, password) VALUES (?, ?)"
        cursor.execute(insert_query, user)
        connection.commit()
        connection.close()

        return ({'messsage': 'user name "{}" created'.format(username)}, 201)