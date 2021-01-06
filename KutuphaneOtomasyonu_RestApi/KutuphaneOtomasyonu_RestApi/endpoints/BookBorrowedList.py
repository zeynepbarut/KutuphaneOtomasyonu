from flask_restful import reqparse, abort, Resource
from endpoints import DBHelper as db


class BookBorrowedList(Resource):
    
    def get(self,user_name):  # Kullanıcının ödünç alıdğı tüm kitapları listeler.
        client = db.create_connection()
        if client == False:
            return "Bağlanılamadı"
        books = db.get_booksBorrowedList(user_name,client) # Ödünç aldığım tum kitapları getir.
        # print(booksList)
        db.close_connection(client)
        return books  # Odunc alınan Kitaplar listesi

