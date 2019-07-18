import sqlite3

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        select_query = 'SELECT * FROM USERS WHERE username = ?'
        result = cursor.execute(select_query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        conn.close()
        return user
