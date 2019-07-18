import sqlite3

conn = sqlite3.connect('data.db')

cursor = conn.cursor()

create_query = 'CREATE TABLE USERS(id int, username text, password text)'
conn.execute(create_query)

user = (1, 'john', 'asdf')
insert_query = 'INSERT INTO USERS VALUES(?, ?, ?)'
conn.execute(insert_query, user)

users = [
(2, 'adam', 'ghjk'),
(3, 'eve', 'zxcv')
]
conn.executemany(insert_query, users)

conn.commit()
conn.close()
