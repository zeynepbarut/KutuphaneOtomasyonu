from flask_restful import reqparse, abort, Resource
from endpoints import DBHelper as db

parser = reqparse.RequestParser()
parser.add_argument('yonetici_adi', type = str)
parser.add_argument('parola', type = str)


class LoginAdmin(Resource):

    def get(self):
        pass

# Giriş işlemi yapıldığında post isteği, giriş başarılı ise true başarısız ise false değer döndürür.
    def post(self):
        client = db.create_connection()
        args = parser.parse_args()
        result = db.login_admin(args.yonetici_adi,args.parola,client)
        db.close_connection(client)
        return result
        
