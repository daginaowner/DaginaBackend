from flask import Blueprint, request
from .generateResp import generateJsonResponse
from .enquiries_service import create_enquiry_service, get_enquiry_service, delete_enquiry_service
import jwt
from dotenv import dotenv_values

# Create a blueprint for enquiry routes
enquiries_route = Blueprint('enquiries_route', __name__)

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

# Create enquiries as they come in
@enquiries_route.route('/enquiries/create', methods=['POST'])
def create_enquiry():
    try:
        data = request.get_json()
        return create_enquiry_service(data)
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))
    
# Get enquiry for particular sellers
@enquiries_route.route('/getenquiries', methods=['POST'])
def get_enquiries():
    try:
        data = request.get_json()
        return get_enquiry_service(data)
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))
    
@enquiries_route.route('/enquiries/delete', methods=['POST'])
def delete_enquiries():
    try:
        tok = request.headers.get('token')
        if tok is None:
            return {"status": "Please provide auth token"}
        auth, msg = decode_token(tok)
        if auth == None:
            return generateJsonResponse(success=False, status=401, message=str(msg))
        else:
            data = request.get_json()
            return delete_enquiry_service(data, auth)
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))