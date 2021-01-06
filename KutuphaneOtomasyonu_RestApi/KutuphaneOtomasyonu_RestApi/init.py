from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

from endpoints import BookBorrowedList
from endpoints import BooksUser
from endpoints import BookOperations
from endpoints import LoginUser
from endpoints import LoginAdmin
from endpoints import RegisterUser
from endpoints import BooksAdmin
from endpoints import BookDelete


app = Flask(__name__)
api = Api(app)

# POST : Kullanıcı veya yönetici girişi kontrol edilir.
api.add_resource(LoginUser.LoginUser,'/login/user')
api.add_resource(LoginAdmin.LoginAdmin,'/login/admin')

# POST : Kullanıcı kaydı oluşturma işlemi
api.add_resource(RegisterUser.RegisterUser,'/register')

# User için işlemler;
# GET : Bütün kitapları görebiliriz.
api.add_resource(BooksUser.BooksUser, '/books/user')


# Admin  için işlemler;
# Post ile bir kitap ekler
api.add_resource(BooksAdmin.BooksAdmin,'/books/admin')

# book_id ye göre kitabı silme işlemi
api.add_resource(BookDelete.BookDelete,'/book/<int:book_id>')



# Kullanıcının ödünc aldığı kitaplar listelenir.
api.add_resource(BookBorrowedList.BookBorrowedList,'/book/<string:user_name>')


# GET : Kitap ödünç alma işlemi 
# DELETE : Kitap teslim etme işlemi
# PUT : Kitap Teslim Tarihini Güncelleme
api.add_resource(BookOperations.BookOperations,'/book/<string:user_name>/<int:book_id>')


if __name__ == '__main__':
    # 192.168.0.102
    # app.run(debug=False, host = '0.0.0.0', port = 9797)
    app.run(debug=False, host = "localhost", port = 9797)
