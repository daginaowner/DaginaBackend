from flask import Blueprint, request
from .userService import buyer_signup_service, seller_signup_service, user_login_service
from pymongo import MongoClient
from dotenv import dotenv_values

config = dotenv_values(".env")
mongo_uri = config.get("MONGO_URI")
db_name = config.get("DB_NAME")

client = MongoClient(mongo_uri)
DB = client.get_default_database(db_name)

user_route = Blueprint('user_route', __name__)

@user_route.route("/api/user/buyer/signup", methods=['POST'])
def buyer_signup():
    data = request.get_json()
    return buyer_signup_service(data,DB)

@user_route.route("/api/user/seller/signup", methods=['POST'])
def seller_signup():
    data = request.get_json()
    return seller_signup_service(data,DB)

"""
In this endpoint 
0 indicates login for Buyer
any other integer indicates login for Seller
"""
@user_route.route("/api/user/login/<int:type>", methods=['POST'])
def buyer_login(type):
    data = request.get_json()
    return user_login_service(data,DB,type)