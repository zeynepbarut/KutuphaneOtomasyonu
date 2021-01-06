from flask_restful import reqparse, abort, Resource
from endpoints import DBHelper as db

parser = reqparse.RequestParser()
parser.add_argument('kullanici_adi', type = str)
parser.add_argument('isim', type = str)
parser.add_argument('soyisim', type = str)
parser.add_argument('parola', type = str)

class RegisterUser(Resource):
    def post(self):
        args = parser.parse_args()
        client = db.create_connection()
        result = db.register(args.kullanici_adi, args.isim,args.soyisim,args.parola,client)
        db.close_connection(client)
        return result
        