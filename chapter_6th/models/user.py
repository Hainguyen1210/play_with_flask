from db import db


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    USERNAME_LENGTH = 80
    PASSWORD_HASH_LENGTH = 100
    username = db.Column(db.String(USERNAME_LENGTH))
    password_hash = db.Column(db.String(PASSWORD_HASH_LENGTH))

    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, uid):
        return cls.query.get(uid)
