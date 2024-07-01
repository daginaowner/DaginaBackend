import bcrypt
import jwt
from dotenv import dotenv_values
import datetime
from .mongo_connect import DB

def generate_token(payload):
    config = dotenv_values(".env")
    secret = config.get("TOKEN_SECRET")
    return jwt.encode(payload, secret, algorithm="HS256")

def encrypt_password(password):
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

def compare_passwords(password, hashed_password):
    if bcrypt.checkpw(password.encode('utf8'), hashed_password):
        return True
    return False

def buyer_signup_service(data):
    try:
        buyer_collection = DB["Buyer"]
        email = data['email']
        if buyer_collection.find_one(filter={"email":email}):
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
        return {"status": "fail", "message": "An error has occured. Please try again!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def seller_signup_service(data):
    try:
        seller_collection = DB["Seller"]
        email = data['email']
        if seller_collection.find_one(filter={"email":email}):
            return {"status":"fail", "message":"This email already exists!"}
        resp = seller_collection.insert_one({
            "email": email,
            "password": encrypt_password(data['password']),
            "phoneNumber": data['phoneNumber'],
            "name": data['name'],
            "address": data['address'],
            "productLimit": 10,
            "productids": [],
            "listOfCategories": [],
            "noOfProfileVisits": 0 
        })
        if resp.inserted_id:
            return {"status": "success", "message": "Seller has been successfully added"}
        return {"status": "fail", "message": "An error has occured. Please try again!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def user_login_service(data, type):
    try:
        collection = None
        if type:
            collection = DB["Seller"]
        else:
            collection = DB["Buyer"]
        email = data['email']
        db_obj = collection.find_one({"email":email},{"_id":1, "email":1, "password":1})
        if db_obj == None:
            return {"status":"fail", 
                    "message":"Account with this email doesn't exist. Please create an account first!"}
        usr_passwd = data['password']
        auth = compare_passwords(usr_passwd, db_obj["password"])
        if auth:
            payload = {'email': db_obj['email'], 
                       '_id': str(db_obj['_id']), 
                       'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=100)
            }
            token = generate_token(payload)
            return {"status": "success", 
                    "token": "Bearer " + token,
                    "type": "Seller" if type else "User",
                    "message": "User has been successfully logged in!"}
        return {"status": "fail", "message": "Please enter correct password"}
    except Exception as e:
        return {"status": "error", "message": str(e)}