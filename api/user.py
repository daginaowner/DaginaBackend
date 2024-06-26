from flask import Blueprint, request
from services.userService import buyer_signup_service,seller_signup_service ,login_service

user_route = Blueprint('user_route', __name__)

@user_route.route("api/user/buyer/signup", methods=['POST'])
def buyer_signup():
    data = request.get_json()
    return buyer_signup_service(data)

@user_route.route("api/user/seller/signup", methods=['POST'])
def seller_signup():
    data = request.get_json()
    return seller_signup_service(data)

@user_route.route("api/user/login", methods=['POST'])
def login():
    data = request.get_json()
    return login_service(data)