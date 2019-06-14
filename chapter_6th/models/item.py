import sqlite3


class ItemModel:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def to_json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query = "SELECT * FROM items WHERE name=?"
        results = cur.execute(query, (name, ))
        row = results.fetchone()
        con.close()

        return cls(row[1], row[2]) if row else None

    def insert(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        insert_query = "INSERT INTO items (name, price) VALUES (?, ?);"
        cursor.execute(insert_query, (self.name, self.price))
        connection.commit()
        connection.close()

    def update(self, new_price):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        update_query = "UPDATE items SET price=? WHERE name=?;"
        cursor.execute(update_query, (new_price, self.name))
        connection.commit()
        connection.close()

    def delete(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        delete_query = "DELETE FROM items WHERE name=?;"
        cursor.execute(delete_query, (self.name,))
        connection.commit()
        connection.close()
