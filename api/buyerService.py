import bcrypt
import jwt
import datetime
from dotenv import dotenv_values
from .mongo_connect import DB
from bson import ObjectId
from .generateResp import generateJsonResponse

buyer_collection = DB["Buyer"]
product_collection = DB["Products"]
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

def buyer_login_service(data):
    try:
        email = data['email']
        db_obj = buyer_collection.find_one({"email": email}, 
            {"_id":1, "email": 1, "password":1})
        if db_obj == None:
            return {"success":False, "data": "Account with this email doesn't exist. Please create an account first!"}
            #return {"status": "Account with this email doesn't exist. Please create an account first!"}
        usr_passwd = data['password']
        auth = compare_passwords(usr_passwd, db_obj["password"])
        #print(db_obj)
        if auth:
            payload = {
                'email': db_obj["email"],
                '_id': str(db_obj["_id"]),
                'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=100)
            }
            token = generate_token(payload)
            return {"success":True, "data": {'token': token, '_id': str(db_obj["_id"])}}
            #return generateJsonResponse(success=True, status=200, message="User login successful", data={'token': token, 'buyer_id': str(db_obj["_id"])})
            #return {"status": token}
        else:
            return {"success":False, "data": "Please enter correct password"}
            #return generateJsonResponse(success=False, status=401, message="Please enter correct password")
            #return {"status": "Please enter correct password"}
    except Exception as e:
        generateJsonResponse(success=True, status=200, message=str(e))

def buyer_signup_service(data):
    try:
        email = data["email"]
        if buyer_collection.find_one(filter={"email":email}):
            return generateJsonResponse(success=False, status=401, message="This email already exists")
            #return {"status": "This email already exists"}
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
            return generateJsonResponse(success=True, status=201, message="User added as a Buyer")
            #return {"status": "User added as Buyer"}
        return generateJsonResponse(success=False, status=400, message="An error occured!")
        #return {"status": "An error occured"}
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))
        #return {"status": str(e)}

def buyer_update_service(data, auth):
    try:
        email = auth['email']
        filters = {"email":email}
        keys = ["fname","lname","phn_no","password","address","city","state","pincode","wishlist","orders"]
        for key in data:
            if key not in keys:
                return generateJsonResponse(success=False, status=401, message="Invalid Key, Please update only valid keys")
                #return {"status": "Invalid Key, Please update only valid keys"}
        if "password" in data:
            data['password'] = encrypt_password(data['password'])
        result = buyer_collection.update_one(filters, {"$set" : data})
        if result.matched_count == 0:
            return generateJsonResponse(success=False, status=401, message="No user matched with this email")
            #return {"status": "No user matched with this email"}
        else:
            return generateJsonResponse(success=True, status=200, message=f"{email} User modified", data={'new_id': {result.upserted_id}})
            #return {"status": f"{email} user modified. New id is {result.upserted_id}"}
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))
        #return {"status": str(e)}

def buyer_delete_service(auth):
    try:
        email = auth['email']
        result = buyer_collection.delete_one(filter={"email":email})
        if result.deleted_count == 1:
            return generateJsonResponse(success=True, status=200, message=f"{email} user deleted")
            #return {"status": f"{email} user deleted"}
        elif result.deleted_count == 0:
            return generateJsonResponse(success=False, status=400, message=f"{email} doesn't exist or cannot be deleted")
            #return {"stauts": f"{email} doesn't exist or cannot be deleted"}
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))
        #return {"status": str(e)}

def buyer_details_service(email):
    try:
        result = buyer_collection.find_one({"email": email},{"password":0})
        if not result:
            return generateJsonResponse(success=False, status=400, message=f"{email} doesn't exists")
            #return {"status": f"{email} doesn't exists"}
        result['_id'] = str(result['_id'])
        return generateJsonResponse(success=True, status=200, message=f"{email} user found", data=result)
        #return {"status": result}
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))
        #return {"status": str(e)}
    
def buyer_wishlist_service(email):
    try:
        result = buyer_collection.find_one({"email":email},{"wishlist":1})
        if not result:
            return generateJsonResponse(success=False, status=400, message=f"{email} doesn't exists")
            #return {"status": f"{email} doesn't exists"}
        del result['_id']
        return generateJsonResponse(success=True, status=200, message=f"{email} user's wishlist", data=result['wishlist'])
        #return {"status": result['wishlist']}
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))
        #return {"status": str(e)}

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
    

#Service for Adding Reviews by Buyers on Products
def buyer_addprodrev_service(data, user_auth):
    try:
        user_id = user_auth['_id']
        prod_id = data['prod_id']
        comment = data['review']
        rating = int(data['rating'])

        #Check if the person adding review is not a seller
        check = seller_collection.find_one({"_id": ObjectId(str(user_id))})
        print(check)
        if check != None:
            return generateJsonResponse(success=False, status=401, message=f"A seller cannot edit reviews")
        #print("Reached here")
        #Creating the Review document which is supposed to be added
        sample = {
            'ratedby': ObjectId(user_id),
            'comment': comment,
            'rating': int(rating)
        }

        #Check Given Rating Range
        if rating > 5 or rating < 1:
            return generateJsonResponse(success=False, status=401, message=f"Please give a rating between 1 and 5")

        #Updating and Adding the review into the reviews array field
        result = product_collection.update_one(
            {'_id': ObjectId(prod_id)},
            {
                "$push" : {
                    "reviews" : sample
                }
            }
        )
        if result.modified_count == 0:
            return generateJsonResponse(success=False, status=401, message=f"Couldn't find the given product {prod_id}")
        return generateJsonResponse(success=True, status=200, message=f"{result.matched_count} Object edited")

    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))
    

#Service for Adding Feedback by Buyers on Seller
def buyer_addsellerrev_service(data, user_auth):
    try:
        user_id = user_auth['_id']
        seller_id = data['seller_id']
        comment = data['review']
        rating = int(data['rating'])

        #Check if the person adding review is not a seller
        check = seller_collection.find_one({"_id": ObjectId(str(user_id))})
        #print(check)
        if check != None:
            return generateJsonResponse(success=False, status=401, message=f"A seller cannot add reviews")
        #print("Reached here")
        #Creating the Review document which is supposed to be added
        sample = {
            'ratedby': ObjectId(user_id),
            'comment': comment,
            'rating': int(rating)
        }

        #Check Given Rating Range
        if rating > 5 or rating < 1:
            return generateJsonResponse(success=False, status=401, message=f"Please give a rating between 1 and 5")

        #Updating and Adding the review into the reviews array field
        result = seller_collection.update_one(
            {'_id': ObjectId(seller_id)},
            {
                "$push" : {
                    "feedback" : sample
                }
            }
        )
        if result.modified_count == 0:
            return generateJsonResponse(success=False, status=401, message=f"Couldn't find the given seller {seller_id}")
        return generateJsonResponse(success=True, status=200, message=f"{result.matched_count} Object edited")

    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))