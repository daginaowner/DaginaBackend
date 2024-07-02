from flask import Blueprint, request
from .product_service import get_products_service,get_categories_products_service,get_price_range_products_service,update_no_of_clicks,get_seller_products_service,get_clicks_products_service

from flask import jsonify



product_route = Blueprint('product_route', __name__)

#getting general products
@product_route.route("/api/products", methods=['GET'])
def get_products():
    try:
        response = get_products_service()
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 

#getting products based on category
@product_route.route("/api/products/category/<string:category>", methods=['GET'])
def get_categories_products(category):
    try:
    
        response =  get_categories_products_service(category)
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#getting products based on price range
@product_route.route("/api/products/pricerange/<string:pricerange>", methods=['GET'])
def get_price_range_products(pricerange):
    try:
        response =  get_price_range_products_service(pricerange)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#getting products based on seller Id
@product_route.route("/api/products/sellerId/<string:sellerId>", methods=['GET'])
def get_seller_products(sellerId):
    try : 
        response =  get_seller_products_service(sellerId)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    

#getting producst based on highest no of clicks
@product_route.route("/api/products/clicks", methods=['GET'])
def get_clicks_products():
    try:
    # data = request.get_json()
        response =  get_clicks_products_service()
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# #getting single product details
# @product_route.route("/api/products/<string:productId>", methods=['GET'])
# def get_price_range_products(productId):
#     return get_product_details_service(productId,DB)

# #finding products details based on search field
# @product_route.route("/api/products/<string:searchInput>", methods=['GET'])
# def get_price_range_products(searchInput):
#     return get_searched_products_service(searchInput,DB)

@product_route.route('/api/products/update_clicks', methods=['POST'])
def update_clicks():
    try:

        data = request.get_json()
        product_id = data.get('productId')
        no_of_clicks = data.get('noOfClicks')
        if not product_id or not no_of_clicks:
          return jsonify({"error": "productId and noOfClicks are required"}), 400


        
        response = update_no_of_clicks( product_id, no_of_clicks)
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500