from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store = db.relationship('StoreModel')
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'store_id': self.store_id
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).order_by(cls.store_id).first()

    @classmethod
    def find_by_id(cls, item_id):
        return cls.query.get(item_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
