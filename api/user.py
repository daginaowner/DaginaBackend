from flask import Blueprint, request
from services.userService import signup_service, login_service

user_route = Blueprint('user_route', __name__)

@user_route.route("api/user/buyer/signup", methods=['POST'])
def buyerSignup():
    data = request.get_json()
    return signup_service(data)

@user_route.route("api/user/seller/signup", methods=['POST'])
def sellerSignup():
    data = request.get_json()
    return login_service(data)

@user_route.route("api/user/login", methods=['POST'])
def login():
    data = request.get_json()
    return login_service(data)