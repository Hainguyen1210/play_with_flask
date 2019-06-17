import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

insert_query_user = "INSERT INTO users (username, password) VALUES (?, ?);"
users = [
    ('jose', 'asdf'), 
    ('hai', 'haha'), 
    ('anotherone', 'haha')
]
cursor.executemany(insert_query_user, users)

insert_query_store = "INSERT INTO stores (name) VALUES (?);"
stores = [
    ('uno', ),
    ('dos', ),
    ('tres', )
]
cursor.executemany(insert_query_store, stores)

insert_query_item = "INSERT INTO items (name, price, store_id) VALUES (?, ?, ?);"
items = [
    ('table', 34, 1), 
    ('car', 200, 2), 
    ('house', 600, 2), 
]
cursor.executemany(insert_query_item, items)

connection.commit()
connection.close()
