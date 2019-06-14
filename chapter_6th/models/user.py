import sqlite3

class UserModel:
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