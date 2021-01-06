from flask_restful import reqparse, abort, Resource
from endpoints import DBHelper as db

parser = reqparse.RequestParser()
parser.add_argument('kullanici_adi', type = str)
parser.add_argument('parola', type = str)



class LoginUser(Resource):

    def get(self):    # Butun Kullanıcılar listelenir.
        client = db.create_connection()
        result = db.getUserList(client)
        db.close_connection(client)
        return result

# Giriş işlemi yapıldığında post isteği, giriş başarılı ise true başarısız ise false değer döndürür.
    def post(self):
        args = parser.parse_args()
        client = db.create_connection()
        result = db.login_user(args.kullanici_adi, args.parola, client)
        db.close_connection(client)
        return result
        
