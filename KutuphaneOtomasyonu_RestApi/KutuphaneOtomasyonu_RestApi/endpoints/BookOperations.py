from flask_restful import reqparse, abort, Resource
from endpoints import DBHelper as db


class BookOperations(Resource):
    
    def get(self,user_name,book_id):  # Kullanıcı bir kitap ödünç alır.
        client = db.create_connection()
        if client == False:
            return "Bağlanılamadı"
        check = db.booksBorrowed(user_name,book_id,client) 
        db.close_connection(client)
        return check  # Kitap odunç alınır.



    def put(self,user_name,book_id):  # Kitap Teslim Tarihi Güncelleme
        client = db.create_connection()
        if client == False:
            return "Bağlanılamadı"
        result = db.update_book_deliver(user_name,book_id,client) 
        db.close_connection(client)
        return result



    def delete(self,user_name,book_id):  # Kitap teslim etme işlemi
        client = db.create_connection()
        if client == False:
            return "Bağlanılamadı"

        result = db.book_deliver(book_id,client) 
        db.close_connection(client)
        return result  # true değer döndürür.
