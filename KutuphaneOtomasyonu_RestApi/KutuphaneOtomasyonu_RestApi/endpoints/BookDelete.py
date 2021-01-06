from flask_restful import reqparse, abort, Resource
from endpoints import DBHelper as db


class BookDelete(Resource):
    
    def delete(self,book_id):  # book_id si girilen kitabı silme işlemi
        client = db.create_connection()
        if client == False:
            return "Bağlanılamadı"
        result = db.bookDelete(book_id,client)
        db.close_connection(client)
        return result  