from flask import Blueprint, request
from .product_service import get_products_service,get_categories_products_service,get_clicks_products_service,get_price_range_products_service,get_product_details_service, get_seller_products_service, get_searched_products_service
from pymongo import MongoClient
from dotenv import dotenv_values

product_route = Blueprint('product_route', __name__)

#getting general products
@product_route.route("api/products", methods=['GET'])
def get_products():
    return get_products_service()

#getting products based on category
@product_route.route("api/products/<string:category>", methods=['GET'])
def get_categories_products(category):
    return get_categories_products_service(category)

#getting products based on price range
@product_route.route("api/products/<string:pricerange>", methods=['GET'])
def get_price_range_products(pricerange):
    return get_price_range_products_service(pricerange)

#getting products based on seller Id
@product_route.route("api/products/<string:sellerId>", methods=['GET'])
def get_seller_products(sellerId):
    return get_seller_products_service(sellerId)

#getting producst based on clicks
@product_route.route("api/products/clicks", methods=['GET'])
def get_clicks_products():
    # data = request.get_json()
    return get_clicks_products_service()

#getting single product details
@product_route.route("api/products/<string:productId>", methods=['GET'])
def get_price_range_products(productId):
    return get_product_details_service(productId)

#finding products details based on search field
@product_route.route("api/products/<string:searchInput>", methods=['GET'])
def get_price_range_products(searchInput):
    return get_searched_products_service(searchInput)