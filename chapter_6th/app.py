from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from resources.item import Item, Items, AllItems
from resources.store import Store, Stores
from resources.user import UserRegister
from security import authenticate, identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'

jwt = JWT(app, authenticate, identity)
api = Api(app)

api.add_resource(Item, '/stores/<int:store_id>/items/<int:item_id>')
api.add_resource(Items, '/stores/<int:store_id>/items')
api.add_resource(AllItems, '/items')

api.add_resource(Store, '/stores/<int:store_id>')
api.add_resource(Stores, '/stores')

api.add_resource(UserRegister, '/register')


@app.before_first_request
def create_table():
    db.create_all()


if __name__ == "__main__":
    from db import db

    db.init_app(app)
    app.run(port=5000, debug=True)
