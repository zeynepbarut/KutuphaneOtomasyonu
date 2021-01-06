import pymongo 
from pymongo import MongoClient
import json
from bson import json_util

import datetime
from datetime import date

import os

def create_connection():
    try:
        # Database 'in ismi Mongodb 'de KutuphaneOtomasyonu şeklinde tanımlandı.---------<dbname> şeklinde yazıldı.
        # Mongodb hesabı oluşturma ve server'a bağlanma kısmı
        client = pymongo.MongoClient('localhost', 27017)
    except Exception as error:
        print(error)
        return False
    return client 

def close_connection(client):
    try:
        client.close()
    except Exception as error:
        print(error)
        return False
    return True



# Kullanıcı girişini kontrol eder.
def login_user(kullanici_adi, parola, client):
    db = client["KutuphaneOtomasyonu"]
    collection = db["Kullanicilar"]

    check = list(collection.find({"parola":parola,"kullanici_adi":kullanici_adi}))

    if(len(check) == 1):
        return  "true"  # Giriş Başarılı
    else:
        return   "false"           #"kullanici_adi veya parola Hatalı" Giriş başarısız

# Yönetici girişini kontrol eder.
def login_admin(yonetici_adi, parola, client):
    db = client["KutuphaneOtomasyonu"]
    collection = db["Yoneticiler"]

    check = list(collection.find({"parola":parola,"yonetici_adi":yonetici_adi}))

    if(len(check) == 1):
        return  "true"   # Giriş Başarılı
    else:
        return  "false"           #"yonetici_adi veya parola Hatalı"


# Kullanici kaydi oluşturulur.
def register(kullanici_adi, isim,soyisim,parola,client):
    db = client["KutuphaneOtomasyonu"]
    collection = db["Kullanicilar"]

    if(len(list(collection.find({"kullanici_adi":kullanici_adi}))) == 1 ): # Kaydetmeden önce kontrol et...
        return "false"  # Kayıt yapılamadı
        #return  "Bu Kullanıcı adı kayıtlıdır. Kullanıcı adını değiştiriniz."
    else:
        # Kayıt yapılır.
        user = {"kullanici_adi":kullanici_adi,"isim":isim,"soyisim":soyisim,"parola":parola}
        collection.insert_one(user)
        return "true"    # "Kayit Yapildi"     
 
def get_all_books(client):
    db = client["KutuphaneOtomasyonu"]
    collection = db["Kitaplar"]
    # Kitaplar tablosundaki olan tüm dokümanları(kayıtları) getirir.
    all_books = list(collection.find({})) 
    return all_books
    
# Butun Kullanıcıları döndürür.
def getUserList(client):
    db = client["KutuphaneOtomasyonu"]
    collection = db["Kullanicilar"]
    # Kullanicilar tablosundaki olan tüm dokümanları(kayıtları) getirir.
    # Bu sorgu SQL deki  (Select kullanici_adi,parola,isim,soyisim from Kullanicilar) sorgusuna eşdeğerdir.     
    all_user = list(collection.find({},{"_id":0})) 
    # all_user = list(collection.find({},{"_id":0}).sort({"kullanici_adi": 1})) 
    return all_user

# Admin kitap ekleme işlemi.
def add_book(_id,kitap_adi,kitap_yazari,kategori_adi,sayfa_sayisi,client):
    db = client["KutuphaneOtomasyonu"]
    collection = db["Kitaplar"]  
    #_id aslında book_id dir. 
    '''
    String'i Tamsayıya Çevirme
    '''
    _id = int(_id)
    book = list(collection.find({"_id":_id}))
    # Kayıt Yapılabilir
    if(len(book) == 0 ):  
        book = {"_id":_id,"kitap_adi":kitap_adi,
            "kitap_yazari":kitap_yazari,"kategori_adi":kategori_adi,"sayfa_sayisi":sayfa_sayisi,
             "kitap_durumu":"Kitap Raftadir" }
        collection.insert_one(book)
        return "true"   # Kitap Kaydedildi
    else:   
        return "false"  # Kitap Kaydedilemedi _id ' yi değiştirin.............


# Admin Kitap Silme işlemi
def bookDelete(book_id,client):
    db = client["KutuphaneOtomasyonu"]
    collection = db["Kitaplar"]
    collection1 = db["Odunc"]  

    book_id = int(book_id)
    book = list(collection1.find({"_id":book_id})) # odunc tablosuna bakılır.

    if(len(book) == 0 ):  # Kitap oduncte değildir . Kitap silinebilir.
        collection.remove({"_id": book_id })
        return "true"
    elif(len(book) == 1):
        # Odunc Tablosunda kitap vardır. Yani kitap ödünctedir. Kitap silinemez.
        return "false"
    
 


def get_booksBorrowedList(user_name,client):  # Kullanıcı ödünç aldığı kitapların listesini görebilir.
    db = client["KutuphaneOtomasyonu"]
    collection = db["Odunc"]    
    collection1 = db["Kitaplar"]

    # user_name kullanıcının odunc aldığı kitapları listeler...
    join = list(collection.aggregate([
        {
            "$lookup":
            {
                "from" : "Kitaplar",
                "localField" : "_id",
                "foreignField":"_id",
                "as": "join"
            }
        },
        { "$match":{"kullanici_adi":user_name}},
        
        {
            "$replaceRoot": { "newRoot": { "$mergeObjects": [ { "$arrayElemAt": [ "$join", 0 ] }, "$$ROOT" ] } }
        },
   { "$project": { "join": 0,"kitap_durumu":0}}
    ]))

    return join

def book_deliver(book_id,client):  # Kitap Teslim edilir.
    db = client["KutuphaneOtomasyonu"]
    collection = db["Kitaplar"]   
    book_id = int(book_id)
    collection.update_one({"_id":book_id},{"$set":{"kitap_durumu":"Kitap Raftadir"}})

    collection1 = db["Odunc"]   
    book_id = int(book_id)   
    # Odunc Tablosun dan da silme işlemi yapılır.
    collection1.delete_one({"_id":book_id})

    return "Kitap Teslim Edildi"

def booksBorrowed(user_name,book_id,client):  # Kullanıcı odunç alma işlemi
    db = client["KutuphaneOtomasyonu"]
    collection = db["Kitaplar"]  
    collection1 = db["Odunc"]  

    # print(type(book_id)) # Bu type fonksiyonu ile değişkenin türünü öğrenebiliriz.book_id string olarak gelir. 
    '''
    String'i Tamsayıya Çevirme
    '''
    book_id = int(book_id)
    book = list(collection1.find({"_id":book_id})) # odunc tablosuna bakılır.

    if(len(book) == 0 ):  # Listedeki eleman sayısı 0 ise Ödünç alınabilir.
        # Kullanıcı bir kitap ödünç aldığında database deki kitap bilgisi değiştirilir.
        today = datetime.date.today()
        today_format = today.strftime("%d.%m.%Y")
        # Kullanıcıyı ödünç tablosuna ekleriz...
        odunc1 = {"_id":book_id,"kullanici_adi":user_name, 
                   "alma_tarihi":today_format,"teslim_tarihi":new_borrowed_date(today)}
        collection1.insert_one(odunc1) # Odunc alındı

        # Aynı zamanda kitaplar tablosunu da güncelleriz. kitap_durumu güncellenir.
        collection.update_one({"_id":book_id},{"$set":{"kitap_durumu":new_borrowed_date(today)}})
        return new_borrowed_date(today)  # Teslim Tarihini döner
       # return "Kitap Ödünç Alındı"
    elif(len(book) == 1):
        # Odunc Tablosunda kitap vardır. Yani kitap ödünctedir
        return "false"
    

def update_book_deliver(user_name,book_id,client): # Teslim tarihi günceller
    db = client["KutuphaneOtomasyonu"]
    collection = db["Kitaplar"]
    collection1 = db["Odunc"]   
    result  = ""
    book_id = int(book_id)
    for x in collection.find({"_id":book_id},{"_id":0,"kitap_durumu":1}):
        result = x["kitap_durumu"]  # Oduncte olan tarihi result'a atadık...
        #print(x)                  x-> "kitap_durumu":"20.11.2020" key ve value olarak  doner
    #print(result)                 result -> "20.11.2020"  value olarak geri doner

    # result parçala --  gun - ay -yıl olarak degiskenlere atanır.
    tarih = result.split(".")
    day1 = int(tarih[0])
    month1 = int(tarih[1])
    year1 = int(tarih[2])
    tarih = date(year1,month1,day1)  #datetime formatına çevrilir.
    
    # Kitaplar tablosu güncellenir.
    collection.update_one({"_id":book_id},{"$set":{"kitap_durumu":new_borrowed_date(tarih)}})
    # Odunç Tablosu güncellenir.
    collection1.update_one({"_id":book_id},{"$set":{"teslim_tarihi":new_borrowed_date(tarih)}})
    
    return new_borrowed_date(tarih)
   # return "Yeni Iade Tarihi: " + new_borrowed_date(tarih) + " tarihine kadar oduncte"



def new_borrowed_date(date): # Yeni iade tarihini geri döner
    '''
    gun = time.strftime("%d")
    ay = time.strftime("%m")
    yil = time.strftime("%Y")
    tarih = gun +"." + ay +"." + yil  # Tarih formatlı biçimdedir. (20.11.2020)
        
    tarih = time.strftime("%d.%m.%Y")  # Tarih formatlı biçimdedir. (20.11.2020)
    '''
    # print(today_format)
    # print(new_borrowed_date_format)

    new_borrowed_date = date + datetime.timedelta(days=15) # 15 gun sonra getirecek
    new_borrowed_date_format = new_borrowed_date.strftime("%d.%m.%Y")

    return new_borrowed_date_format



