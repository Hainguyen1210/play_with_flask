from flask_restful import Resource, reqparse, inputs
from werkzeug.security import generate_password_hash

from models.user import UserModel
from my_utils import make_response_message


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username', type=inputs.regex('^\S{4,20}$'), required=True,
        help='Must be 4-20 non-whitespace characters long', trim=True
    )
    parser.add_argument(
        'password', type=inputs.regex('^.{8,20}$'), required=True,
        help='Must be 8-20 characters long', trim=True)

    def post(self):
        request_data = self.parser.parse_args()
        username = request_data.get('username')
        password = request_data.get('password')

        # Users cannot have the same name
        if UserModel.find_by_username(username):
            return make_response_message("User name '{}' already exists".format(username), 400)

        user = UserModel(username, generate_password_hash(password))
        user.save_to_db()
        return make_response_message("User name '{}' created".format(username), 201)
