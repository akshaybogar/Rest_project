import sqlite3

conn = sqlite3.connect('data.db')

cursor = conn.cursor()

create_query = 'CREATE TABLE IF NOT EXISTS USERS(id INTEGER PRIMARY KEY, username text, password text)'
conn.execute(create_query)

conn.commit()
conn.close()
