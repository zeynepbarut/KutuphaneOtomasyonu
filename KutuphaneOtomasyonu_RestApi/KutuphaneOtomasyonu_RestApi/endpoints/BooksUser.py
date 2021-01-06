from flask_restful import reqparse, abort, Resource
from endpoints import DBHelper as db

class BooksUser(Resource):
    
    def get(self): # Butun Kitaplar listelenir.
       
        client = db.create_connection()
        if client == False:
            return "Bağlanılamadı" 
        # get_all_books() metodu ile veri tabanında kayıtlı olan tüm kitaplar json formatında geri döner.
        booksList = db.get_all_books(client)
        #print(booksList)
        db.close_connection(client)

        # Mongodb'de her kayıt bir doküman olarak ifade edilir.
        # Bu dokümanlar Json formatı şeklinde saklanır.
        return booksList
   