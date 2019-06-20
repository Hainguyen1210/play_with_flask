from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def to_json_simple(self):
        return {
            'name': self.name,
            'id': self.id,
        }

    def to_json_with_items(self):
        return {
            'name': self.name,
            'id': self.id,
            'items': [item.to_json() for item in self.items.all()]
        }

    def find_item(self, item_id):
        for item in self.items:
            if item.id == item_id:
                return item

    @classmethod
    def find_by_id(cls, store_id):
        return cls.query.get(store_id)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, store_id):
        return cls.query.filter_by(id=store_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
