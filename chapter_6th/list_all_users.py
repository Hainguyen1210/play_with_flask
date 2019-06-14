import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

list_query = "SELECT * FROM users;"
results = cursor.execute(list_query)

for row in results:
    print(row)

connection.commit()
connection.close()