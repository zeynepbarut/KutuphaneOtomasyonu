http://localhost:9797/

# KUTUPHANE OTOMASYONU SİSTEMİ DOKÜMANTASYONU


## Endpoints 


### GET \- /login/user

Var olan tüm kullanıcıları getirir.

### Örnek Link

`http://localhost:9797/login/user`



### POST\- /login/user

Kullanıcı girişi.

#### Örnek Link

`http://localhost:9797/login/user`

Parametreler;
1) kullanici_adi
2) parola


### POST\- /login/admin

Yönetici girişi.

#### Örnek Link

`http://localhost:9797/login/admin`

Parametreler;
1) yonetici_adi
2) parola



### POST\- /login/register

Yeni bir kullanıcı ekleme işlemi.

#### Örnek Link

`http://localhost:9797/login/register`

Parametreler;
1) kullanici_adi
2) isim
3)soyisim
4)parola



### GET \- /books/user

Var olan tüm kitapları getirir.

### Örnek Link

`http://localhost:9797/books/user`




### POST\- /books/admin

Yeni bir kitap eklemek.

#### Örnek Link

`http://localhost:9797/books/admin`

Parametreler;
1) kitap_adi
2) kitap_yazari
3)kategori_adi
4)sayfa_sayisi



### DELETE\- /book/<int:book_id>

İstenilen kitabı siler.


#### Örnek Link

`http://localhost:9797/book/<int:book_id>`




### GET\- /book/<string:user_name>

Kişinin ödünç almış olduğu kitapları getirir.

#### Örnek Link

`http://localhost:9797/book/ahmet`



### GET\- /book/<string:user_name>/<int:book_id>

Kişinin kitap ödünç alma işlemini.

#### Örnek Link

`http://localhost:9797/book/ahmet/1`



### PUT\- /book/<string:user_name>/<int:book_id>

Kişinin kitap teslim tarihini güncelleme işlemi.

#### Örnek Link

`http://localhost:9797/book/ahmet/1`


### DELETE\- /book/<string:user_name>/<int:book_id>

Kişinin kitap teslim etme işlemi.

#### Örnek Link

`http://localhost:9797/book/ahmet/1`