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

        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        insert_query = 'INSERT INTO ITEMS VALUES(?, ?)'
        cursor.execute(insert_query, (item['name'], item['price']))
        conn.commit()
        conn.close()

        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name']!=name, items))
        return {'message':'Item deleted'}

    def put(self, name):
        data = Item.request_parser.parse_args()
        item = next(filter(lambda x: x['name']==name, items),None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)  #Careful
        return item

class ItemList(Resource):
    def get(self):
        return {'items': items}
