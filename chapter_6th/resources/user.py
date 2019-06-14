import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


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
        if UserModel.find_by_username(username):
            return ({'messsage': 'user name "{}" alredy exists'.format(username)}, 400)

        user = UserModel(username, password)
        user.save_to_db()
        return ({'messsage': 'user name "{}" created'.format(username)}, 201)