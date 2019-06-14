import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

# CREATE USER TABLE
create_table_user = "CREATE TABLE IF NOT EXISTS users (\
        id INTEGER PRIMARY KEY, \
        username text NOT NULL, \
        password text NOT NULL);"

cursor.execute(create_table_user)

insert_query_user = "INSERT INTO users (username, password) VALUES (?, ?);"
users = [
    ('jose', 'asdf'), 
    ('hai', 'haha'), 
    ('haha', 'asdf')
]
cursor.executemany(insert_query_user, users)

# CREATE ITEM TABLE 
create_table_item = "CREATE TABLE IF NOT EXISTS items (\
        id INTEGER PRIMARY KEY, \
        name text NOT NULL, \
        price REAL NOT NULL);"

cursor.execute(create_table_item)

insert_query_item = "INSERT INTO items (name, price) VALUES (?, ?);"
items = [
    ('table', 34), 
    ('car', 200), 
    ('house', 600), 
]
cursor.executemany(insert_query_item, items)

# list_query = "SELECT * FROM users;"
# results = cursor.execute(list_query)
# 
# print(results)
# for row in results:
#     print(row)
# 
connection.commit()
connection.close()