import bcrypt

def encrypt_password(password):
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

def compare_passwords(password, hashed_password):
    if bcrypt.checkpw(password.encode('utf8'), hashed_password):
        return True
    return False

def buyer_signup_service(data,client):
    try:
        buyer_collection = client["Buyer"]
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

def seller_signup_service(data, client):
    try:
        seller_collection = client["Seller"]
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

def user_login_service(data, client, type):
    try:
        collection = None
        if type:
            collection = client["Seller"]
        else:
            collection = client["Buyer"]
        email = data['email']
        dp_passwd = collection.find_one({"email":email},{"_id":0, "password":1})
        if dp_passwd == None:
            return {"status":"fail", 
                    "message":"Account with this email doesn't exist. Please create an account first!"}
        usr_passwd = data['password']
        auth = compare_passwords(usr_passwd, dp_passwd["password"])
        if auth:
            return {"status": "success", "type": "Seller" if type else "User", "message": "User has been successfully logged in!"}
        return {"status": "fail", "message": "Please enter correct password"}
    except Exception as e:
        return {"status": "error", "message": str(e)}