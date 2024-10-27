from flask import Blueprint, request
from .sellerService import seller_signup_service, seller_login_service, seller_update_service, seller_delete_service, seller_details_service, seller_feedback_service, seller_get_products, get_sellers_service
from .mongo_connect import DB
from flask import request
from dotenv import dotenv_values
import jwt
from .generateResp import generateJsonResponse

seller_route = Blueprint('seller_route', __name__)

def decode_token(token):
    decoded_payload = None
    try:
        config = dotenv_values(".env")
        secret = config.get("TOKEN_SECRET")
        decoded_payload = jwt.decode(token, secret, algorithms=["HS256"])
        return decoded_payload , {}
    except jwt.ExpiredSignatureError:
        return decoded_payload, {"status": "Token Expired"}
    except jwt.InvalidTokenError:
        return decoded_payload, {"status": "Token Invalid"}

@seller_route.route("/seller/signup", methods=['POST'])
def seller_signup():
    try:
        data = request.get_json()
        return seller_signup_service(data)
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))
        #return {"status": str(e)}

@seller_route.route("/seller/login", methods=['POST'])
def seller_login():
    try:
        data = request.get_json()
        return seller_login_service(data)
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))


@seller_route.route("/seller/update", methods=['PUT'])
def seller_update():
    try:
        tok = request.headers.get('token')
        if tok is None:
            return {"status": "Please provide auth token"}
        auth, msg = decode_token(tok)
        if auth == None:
            return generateJsonResponse(success=False, status=401, message=str(msg))
        else:
            data = request.get_json()
            return seller_update_service(data, auth)
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))

@seller_route.route("/seller/delete", methods = ['DELETE'])
def seller_delete():
    try:
        tok = request.headers.get('token')
        if tok is None:
            return {"status": "Please provide auth token"}
        auth, msg = decode_token(tok)
        if auth == None:
            return msg
        else:
            return seller_delete_service(auth)
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))

@seller_route.route("/seller/details/<string:seller_id>", methods=['GET'])
def seller_details(seller_id):
    try:
        return seller_details_service(seller_id)
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))

@seller_route.route("/seller/feedbacks/<string:seller_id>", methods=['GET'])
def seller_feedbacks(seller_id):
    try:
        return seller_feedback_service(seller_id)
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))

@seller_route.route("/seller/getProducts/<string:seller_id>", methods=['GET'])
def seller_getdetails(seller_id):
    try:
        return seller_get_products(seller_id)
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))

@seller_route.route("/sellers", methods=['GET'])
def get_sellers():
    try:
        query_params = request.args.to_dict()  # Convert query parameters to a dictionary
        return get_sellers_service(query_params)
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))