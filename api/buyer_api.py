from flask import Blueprint, request
from .buyerService import buyer_signup_service, buyer_login_service, buyer_update_service, buyer_delete_service, buyer_details_service, buyer_wishlist_service, buyer_wishlist_add_service, buyer_wishlist_rem_service
from .mongo_connect import DB
from flask import request
from dotenv import dotenv_values
import jwt
from .generateResp import generateJsonResponse

buyer_route = Blueprint('buyer_route', __name__)

def decode_token(token):
    decoded_payload = None
    try:
        config = dotenv_values(".env")
        secret = config.get("TOKEN_SECRET")
        decoded_payload = jwt.decode(token, secret, algorithms=["HS256"])
        return decoded_payload , {}
    except jwt.ExpiredSignatureError:
        return decoded_payload, "Token Expired"
    except jwt.InvalidTokenError:
        return decoded_payload, "Token Invalid"

@buyer_route.route("/buyer/signup", methods=['POST'])
def buyer_signup():
    try:
        data = request.get_json()
        return buyer_signup_service(data)
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))

@buyer_route.route("/buyer/login", methods=['POST'])
def buyer_login():
    try:
        data = request.get_json()
        return buyer_login_service(data)
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))

@buyer_route.route("/buyer/update", methods=['PUT'])
def buyer_update():
    try:
        tok = request.headers.get('token')
        if tok is None:
            return generateJsonResponse(success=False, status=400, message="Please provide auth token")
            #return {"status": "Please provide auth token"}
        auth, msg = decode_token(tok)
        if auth == None:
            return generateJsonResponse(success=False, status=400, message=msg)
            #return msg
        else:
            data = request.get_json()
            return buyer_update_service(data, auth)
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))

@buyer_route.route("/buyer/delete", methods = ['DELETE'])
def buyer_delete():
    try:
        tok = request.headers.get('token')
        if tok is None:
            return generateJsonResponse(success=False, status=401, message="Please provide auth token")
            #return {"status": "Please provide auth token"}
        auth, msg = decode_token(tok)
        if auth == None:
            return generateJsonResponse(success=False, status=400, message=msg)
            #return msg
        else:
            return buyer_delete_service(auth)
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))

@buyer_route.route("/buyer/details/<string:email>", methods=['GET'])
def buyer_details(email):
    try:
        return buyer_details_service(email)
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))

@buyer_route.route("/buyer/wishlist/<string:email>", methods=['GET'])
def buyer_wishlist(email):
    try:
        return buyer_wishlist_service(email)
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))

@buyer_route.route("/buyer/wishlist/add/<string:prod_id>", methods=['PUT'])
def buyer_wishlist_add(prod_id):
    try:
        tok = request.headers.get('token')
        if tok is None:
            return {"status": "Please provide auth token"}
        auth, msg = decode_token(tok)
        if auth == None:
            return msg
        else:
            return buyer_wishlist_add_service(prod_id, auth)
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))

@buyer_route.route("/buyer/wishlist/remove/<string:prod_id>", methods=['PUT'])
def buyer_wishlist_remove(prod_id):
    try:
        tok = request.headers.get('token')
        if tok is None:
            return {"status": "Please provide auth token"}
        auth, msg = decode_token(tok)
        if auth == None:
            return msg
        else:
            return buyer_wishlist_rem_service(prod_id, auth)
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))