import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):
    request_parser = reqparse.RequestParser()
    request_parser.add_argument('price',
    type = float,
    required = True,
    help = 'Enter price of the item')

    @classmethod
    def find_by_name(cls, name):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = 'SELECT * FROM ITEMS WHERE name = ?'
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        conn.close()
        if row:
            return {'item':{'name':row[0], 'price':row[1]}}


    @jwt_required()
    def get(self,name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if(self.find_by_name(name)):
            return {'message':'Item with {} name already exists'.format(name)}, 400

        data = Item.request_parser.parse_args()
        item = {'name': name, 'price':data['price']}
        try:
            self.insert(item)
        except:
            return {'message':'An error occured'}, 500

        return item, 201

    @classmethod
    def insert(cls, item):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        insert_query = 'INSERT INTO ITEMS VALUES(?, ?)'
        cursor.execute(insert_query, (item['name'], item['price']))
        conn.commit()
        conn.close()

    def delete(self, name):
        item = self.find_by_name(name)
        if not item:
            return {'message': 'Item with given username does not exist'}
        else:
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()
            delete_query = 'DELETE FROM ITEMS WHERE name=?'
            cursor.execute(delete_query, (name,))
            conn.commit()
            conn.close()
            return {'message':'Item deleted'}

    def put(self, name):
        data = Item.request_parser.parse_args()
        item = self.find_by_name(name)
        update_item = {'name': name, 'price': data['price']}
        if item is None:
            try:
                self.insert(update_item)
            except:
                return {'message': 'An error occured'}, 500
        else:
            try:
                self.update(update_item)
            except:
                return {'message':'An error occured'}, 500

        return update_item

    @classmethod
    def update(cls, item):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        update_query = 'UPDATE ITEMS SET price=? WHERE name=?'
        cursor.execute(update_query, (item['price'],item['name']))
        conn.commit()
        conn.close()
        return {'message':'Item deleted'}

class ItemList(Resource):
    def get(self):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        query = 'SELECT * FROM ITEMS'
        result = cursor.execute(query).fetchall()
        items = []
        for row in result:
            items.append({'name':row[0], 'price':row[1]})

        conn.commit()
        conn.close()

        return {'items':items}
