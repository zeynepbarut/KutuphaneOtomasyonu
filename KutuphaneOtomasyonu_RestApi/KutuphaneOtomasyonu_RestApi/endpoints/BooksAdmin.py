from flask_restful import reqparse, abort, Resource
from endpoints import DBHelper as db


parser = reqparse.RequestParser()
parser.add_argument('_id', type = str)
parser.add_argument('kitap_adi', type = str)
parser.add_argument('kitap_yazari', type = str)
parser.add_argument('kategori_adi', type = str)
parser.add_argument('sayfa_sayisi', type = str)

class BooksAdmin(Resource):
        
    def post(self):   # Yeni bir kitap ekle 
        
        args = parser.parse_args()
        client = db.create_connection()
        result = db.add_book(args._id,args.kitap_adi,args.kitap_yazari,args.kategori_adi,args.sayfa_sayisi,client)
        db.close_connection(client)
        return result
        
