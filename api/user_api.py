from flask import Blueprint, request
from .userService import buyer_signup_service, seller_signup_service, user_login_service
from .mongo_connect import DB

user_route = Blueprint('user_route', __name__)

@user_route.route("/buyer/signup", methods=['POST'])
def buyer_signup():
    data = request.get_json()
    return buyer_signup_service(data)

@user_route.route("/api/user/seller/signup", methods=['POST'])
def seller_signup():
    data = request.get_json()
    return seller_signup_service(data)

@user_route.route("/buyer/login", methods=['POST'])
def buyer_login(type):
    data = request.get_json()
    return user_login_service(data,type)