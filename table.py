import sqlite3

conn = sqlite3.connect('data.db')

cursor = conn.cursor()

create_query = 'CREATE TABLE IF NOT EXISTS USERS(id INTEGER PRIMARY KEY, username text, password text)'
cursor.execute(create_query)

create_query = 'CREATE TABLE IF NOT EXISTS ITEMS(name text, price real)'
cursor.execute(create_query)

insert_query = 'INSERT INTO ITEMS VALUES("test_item", 9.99)'
cursor.execute(insert_query)

conn.commit()
conn.close()
