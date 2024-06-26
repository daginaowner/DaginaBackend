#from ..app import DB
import bcrypt


from pymongo import MongoClient
from dotenv import dotenv_values


config = dotenv_values(".env")
mongo_uri = config.get("MONGO_URI")
client = MongoClient(mongo_uri)
DB = client.get_default_database("DaginaDB")


print("Connected to MongoDB")


def encrypt_password(password):
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())


def buyer_signup(data):
    buyer_collection = DB["Buyer"]
    email = data['email']
    results = buyer_collection.find_one(filter={"email":email})
    if results:
        return {"status":"fail", "message":"This email already exists!"}


    resp = buyer_collection.insert_one({
        "email": email,
        "password": encrypt_password(data['password']),
        "phoneNumber": data['phoneNumber'],
        "name": data['name'],
        "address": data['address']
    })
    if resp.inserted_id:
        return {"status": "success", "message": "User has been successfully added"}
    else:
        return {"status": "fail", "message": "An error has occured. Please try again!"}
   
data = {
  "email": "user1@example.com",
  "password": "securepassword123",
  "phoneNumber": "+12345678901",
  "name": "John Doe",
  "address": "123 Main St, Anytown, USA"
}


kk = buyer_signup(data)
print(kk)
