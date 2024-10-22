import bcrypt
import jwt
import datetime
from dotenv import dotenv_values
from .mongo_connect import DB
from bson import ObjectId
import re
import unicodedata
from .generateResp import generateJsonResponse

#Converts data into slug text
def slugify(text):
    # Normalize and decode the string
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    # Replace non-alphanumeric characters with hyphens
    text = re.sub(r'[^\w\s-]', '', text)
    # Convert spaces to hyphens
    text = re.sub(r'\s+', '-', text)
    # Remove leading/trailing hyphens
    text = text.strip('-')
    # Convert to lowercase
    text = text.lower()
    return text

seller_collection = DB["Seller"]
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

def seller_login_service(data):
    try:
        email = data['email']
        db_obj = seller_collection.find_one({"email": email}, 
            {"_id":1, "email": 1, "password":1})
        if db_obj == None:
            return generateJsonResponse(success=False, status=401, message="Account with this email doesn't exist. Please create an account first!")
            #return {"status": "Account with this email doesn't exist. Please create an account first!"}
        usr_passwd = data['password']
        auth = compare_passwords(usr_passwd, db_obj["password"])
        if auth:
            payload = {
                'email': db_obj["email"],
                '_id': str(db_obj["_id"]),
                'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=100)
            }
            token = generate_token(payload)
            return generateJsonResponse(success=True, status=200, message="Login successful", data={'token': token})
            #return {"status": token}
        else:
            return generateJsonResponse(success=False, status=401, message="Please enter correct password")
            #return {"status": "Please enter correct password"}
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))
        #return {"status": str(e)}

def seller_signup_service(data):
    try:
        email = data["email"]
        if seller_collection.find_one(filter={"email":email}):
            return generateJsonResponse(success=False, status=401, message="This email already exists")
            #return {"status": "This email already exists"}
        resp = seller_collection.insert_one({
            "user_details":{
                "fname": data["fname"],
                "lname": data["lname"],
                "recovery_mail": data["recovery_mail"],
                "phn_no": data["phone"]
            },
            "profile_pic": data["profile_pic"],
            "email": email,
            "password": encrypt_password(data["password"]),
            "store_name": data['storename'],
            "store_slug": slugify(data['storename']),
            "address": data["address"],
            "city": data["city"],
            "state": data["state"],
            "pincode": data["pincode"],
            "gstin_no": data["gst"],
            "gmap": {
                "longitudes": data['longitudes'],
                "latitudes": data['latitudes']
            },
            "is_verified": False,
            "images": data["images"],
            "feedback": [],
            "created_at": datetime.datetime.now(),
            "last_updated": datetime.datetime.now(),
        })
        if resp.inserted_id:
            return generateJsonResponse(success=True, status=201, message="User added as seller")
            #return {"status": "User added as Seller"}
        return {"status": "An error occured"}
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))
        #return {"status": str(e)}

def seller_update_service(data, auth):
    try:
        email = auth['email']
        filters = {"email":email}
        keys = ["user_details.fname","user_details.lname","user_details.recovery_mail","user_details.phn_no",
                "profile_pic","password","store_name","city","state","pincode","gstin_no",
                "gmap.longitudes", "gmap.latitudes", "is_verified", "images"]
        for key in data:
            if key not in keys:
                return generateJsonResponse(success=False, status=401, message="Invalid Key, Please update only valid keys")
                #return {"status": "Invalid Key, Please update only valid keys"}
        if "store_name" in data:
            data["store_slug"] = slugify(data["store_name"])
        if "password" in data:
            data["password"] = encrypt_password(data["password"])
        result = seller_collection.update_one(filters, {"$set" : data})
        if result.matched_count == 0:
            return generateJsonResponse(success=False, status=401, message="No user matched with this email")
            #return {"status": "No user matched with this email"}
        else:
            return generateJsonResponse(success=True, status=200, message=f"{email} user modified.", data={'new_id': {result.upserted_id}})
            #return {"status": f"{email} user modified. New id is {result.upserted_id}"}
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))
        #return {"status": str(e)}

def seller_delete_service(auth):
    try:
        email = auth['email']
        result = seller_collection.delete_one(filter={"email":email})
        if result.deleted_count == 1:
            return generateJsonResponse(success=True, status=200, message=f"{email} seller deleted")
            #return {"status": f"{email} seller deleted"}
        elif result.deleted_count == 0:
            return generateJsonResponse(success=False, status=400, message=f"{email} doesn't exist or cannot be deleted")
            #return {"stauts": f"{email} doesn't exist or cannot be deleted"}
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))
        #return {"status": str(e)}

#Returns every detail except feedback about sellers
def seller_details_service(sel_id):
    try:
        result = seller_collection.find_one({"_id": ObjectId(sel_id)},{"password":0, "feedback":0})
        if not result:
            return generateJsonResponse(success=False, status=400, message=f"{sel_id} doesn't exists")
            #return {"status": f"{sel_id} doesn't exists"}
        result['_id'] = str(result['_id'])
        return generateJsonResponse(success=True, status=200, message="", data={'data': result})
        #return {"status": result}
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))
        #return {"status": str(e)}
    
def seller_feedback_service(sel_id):
    try:
        pipeline = [
                {
                    '$match': {
                        '_id': ObjectId(sel_id)
                        }
                },
                {
                    '$unwind': {
                        'path': '$feedback'
                    }
                }, {
                    '$lookup': {
                        'from': 'Buyer', 
                        'localField': 'feedback.owner', 
                        'foreignField': '_id', 
                        'as': 'feedbackowner'
                    }
                }, {
                    '$project': {
                        'feedback': {
                            'owner': '$feedbackowner.fname', 
                            'comment': '$feedback.comment', 
                            'rating': '$feedback.rating'
                        }, 
                        '_id': 1
                    }
                }, {
                    '$group': {
                        '_id': '$_id', 
                        'reviews': {
                            '$push': {
                                'owner': '$feedback.owner', 
                                'comment': '$feedback.comment', 
                                'rating': '$feedback.rating'
                            }
                        }
                    }
                }
            ]
        result = list(seller_collection.aggregate(pipeline))
        if len(result) == 0:
            return generateJsonResponse(success=False, status=400, message=f"{sel_id} Seller doesn't exists")
            #return {"status": f"{sel_id} Seller doesn't exists"}
        arr = []
        for view in result:
            del view['_id']
            arr.append(view)
        return generateJsonResponse(success=True, status=200, message="", data={'feedbacks': arr})
        #return {"status": arr}
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))
        #return {"status": str(e)}
    


