from flask import Blueprint, request
from services.product_services import get_products_service,get_categories_products_service,get_clicks_products_service,get_price_range_products_service,get_product_details_service
from pymongo import MongoClient
from dotenv import dotenv_values

config = dotenv_values(".env")
mongo_uri = config.get("MONGO_URI")
db_name = config.get("DB_NAME")

client = MongoClient(mongo_uri)
DB = client.get_default_database(db_name)

produc_route = Blueprint('product_route', __name__)


#getting general products
@produc_route.route("api/products", methods=['GET'])
def get_products():
    # data = request.get_json()
    return get_products_service()

#getting products based on category
@produc_route.route("api/products/<string:category>", methods=['GET'])
def get_categories_products(category):
    # data = request.get_json()
    return get_categories_products_service(category,DB)

#getting products based on price range
@produc_route.route("api/products/<string:pricerange>", methods=['GET'])
def get_price_range_products(pricerange):
    return get_price_range_products_service(pricerange,DB)

#getting products based on seller Id
@produc_route.route("api/products/<string:sellerId>", methods=['GET'])
def get_seller_products(sellerId):
    return get_seller_products_service(sellerId,DB)

#getting producst based on clicks
@produc_route.route("api/products/clicks", methods=['GET'])
def get_clicks_products():
    # data = request.get_json()
    return get_clicks_products_service(DB)

#getting single product details
@produc_route.route("api/products/<string:productId>", methods=['GET'])
def get_price_range_products(productId):
    return get_product_details_service(productId,DB)

#finding products details based on search field
@produc_route.route("api/products/<string:searchInput>", methods=['GET'])
def get_price_range_products(searchInput):
    return get_searched_products_service(searchInput,DB)