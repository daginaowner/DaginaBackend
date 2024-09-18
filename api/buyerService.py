import bcrypt
import jwt
import datetime
from dotenv import dotenv_values
from .mongo_connect import DB
from bson import ObjectId

buyer_collection = DB["Buyer"]
config = dotenv_values(".env")

def generate_token(payload):
    secret = config.get("TOKEN_SECRET")
    return jwt.encode(payload, secret, algorithm="HS256")

def encrypt_password(password):
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

def compare_passwords(password, hashed_password):
    if bcrypt.checkpw(password.encode('utf8'), hashed_password):
        return True
    return False

def buyer_login_service(data):
    try:
        email = data['email']
        db_obj = buyer_collection.find_one({"email": email}, 
            {"_id":1, "email": 1, "password":1})
        if db_obj == None:
            return {"status": "Account with this email doesn't exist. Please create an account first!"}
        usr_passwd = data['password']
        auth = compare_passwords(usr_passwd, db_obj["password"])
        if auth:
            payload = {
                'email': db_obj["email"],
                '_id': str(db_obj["_id"]),
                'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=100)
            }
            token = generate_token(payload)
            return {"status": token}
        else:
            return {"status": "Please enter correct password"}
    except Exception as e:
        return {"status": str(e)}

def buyer_signup_service(data):
    try:
        email = data["email"]
        if buyer_collection.find_one(filter={"email":email}):
            return {"status": "This email already exists"}
        resp = buyer_collection.insert_one({
            "email": email,
            "fname": data["fname"],
            "lname": data["lname"],
            "phn_no": data["phone"],
            "password": encrypt_password(data["password"]),
            "address": data["address"],
            "city": data["city"],
            "state": data["state"],
            "pincode": data["pincode"],
            "wishlist": [],
            "orders": [],
        })
        if resp.inserted_id:
            return {"status": "User added as Buyer"}
        return {"status": "An error occured"}
    except Exception as e:
        return {"status": str(e)}

def buyer_update_service(data, auth):
    try:
        email = auth['email']
        filters = {"email":email}
        keys = ["fname","lname","phn_no","password","address","city","state","pincode","wishlist","orders"]
        for key in data:
            if key not in keys:
                return {"status": "Invalid Key, Please update only valid keys"}
        if "password" in data:
            data['password'] = encrypt_password(data['password'])
        result = buyer_collection.update_one(filters, {"$set" : data})
        if result.matched_count == 0:
            return {"status": "No user matched with this email"}
        else:
            return {"status": f"{email} user modified. New id is {result.upserted_id}"}
    except Exception as e:
        return {"status": str(e)}

def buyer_delete_service(auth):
    try:
        email = auth['email']
        result = buyer_collection.delete_one(filter={"email":email})
        if result.deleted_count == 1:
            return {"status": f"{email} user deleted"}
        elif result.deleted_count == 0:
            return {"stauts": f"{email} doesn't exist or cannot be deleted"}
    except Exception as e:
        return {"status": str(e)}
    pass

def buyer_details_service(email):
    try:
        result = buyer_collection.find_one({"email": email},{"password":0})
        if not result:
            return {"status": f"{email} doesn't exists"}
        result['_id'] = str(result['_id'])
        return {"status": result}
    except Exception as e:
        return {"status": str(e)}
    
def buyer_wishlist_service(email):
    try:
        result = buyer_collection.find_one({"email":email},{"wishlist":1})
        if not result:
            return {"status": f"{email} doesn't exists"}
        del result['_id']
        return {"status": result['wishlist']}
    except Exception as e:
        return {"status": str(e)}

def buyer_wishlist_add_service(prod_id, auth):
    try:
        email = auth['email']
        arr = buyer_collection.update_one({"email":email}, 
                                          {'$addToSet': {
                                              'wishlist': ObjectId(prod_id)
                                          }})
        if arr.matched_count == 0:
            return {"status": f"{email} doesn't exists"}
        else:
            return {"status": f"{prod_id} added to wishlist"}
    except Exception as e:
        return {"status": str(e)}
    
def buyer_wishlist_rem_service(prod_id, auth):
    try:
        email = auth['email']
        arr = buyer_collection.update_one({"email":email}, 
                                          {'$pull': {
                                              'wishlist': ObjectId(prod_id)
                                          }})
        if arr.matched_count == 0:
            return {"status": f"{email} doesn't exists"}
        else:
            return {"status": f"{prod_id} removed from wishlist"}
    except Exception as e:
        return {"status": str(e)}