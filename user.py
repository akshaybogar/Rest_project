import sqlite3
from flask_restful import Resource, reqparse

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

    @classmethod
    def find_by_id(cls, _id):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        select_query = 'SELECT * FROM USERS WHERE id = ?'
        result = cursor.execute(select_query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        conn.close()
        return user

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type = str,
        required = True,
        help = 'Username cannot be blank'
    )
    parser.add_argument('password',
        type = str,
        required = True,
        help = 'Password cannot be blank'
    )
    def post(self):
        data = UserRegister.parser.parse_args()
        if User.find_by_username(data['username']):
            return {'message':'Username already exists'},400

        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        query = 'INSERT INTO USERS VALUES(NULL, ?, ?)'
        conn.execute(query, (data['username'], data['password']))

        conn.commit()
        conn.close()

        return {'message':'User created successfully'},201
