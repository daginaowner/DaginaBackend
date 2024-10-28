from flask import Blueprint, request, jsonify
from .product_service import get_products_service,get_products_by_ids_service,get_product_by_id_service, create_product_service, delete_product_service, update_product_service
import jwt
from dotenv import dotenv_values
from .generateResp import generateJsonResponse

# Create a blueprint for product routes
product_route = Blueprint('product_route', __name__)

#Function for decoding the token
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

@product_route.route('/getproducts', methods=['GET'])
def get_products():
    try:
        # Extract query parameters from the request (for filtering, sorting, pagination, etc.)
        query_params = request.args.to_dict()  # Convert query parameters to a dictionary
        
        # Call the service function and pass the query parameters
        products = get_products_service(query_params)

        return jsonify(products), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Route to get individual product details by ID
@product_route.route('/getproduct_by_id/<product_id>', methods=['GET'])
def get_product_by_id(product_id):
    try:
        product = get_product_by_id_service(product_id)  # Call service to fetch product by ID
        if product:
            return jsonify(product), 200
        else:
            return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Route to get multiple products by an array of IDs
@product_route.route('/getproduct_by_ids', methods=['POST'])
def get_products_by_ids():
    try:
        # Expect an array of product IDs in the request body
        data = request.get_json()
        product_ids = data.get('product_ids')
        
        if not product_ids:
            return jsonify({'error': 'product_ids is required and should be a list of IDs'}), 400
        
        # Call the service function to fetch products by IDs
        products = get_products_by_ids_service(product_ids)
        
        if products:
            return jsonify(products), 200
        else:
            return jsonify({'error': 'No products found for the given IDs'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Route to create a new product
@product_route.route('/products/create', methods=['POST'])
def create_product():
    try:
        tok = request.headers.get('token')
        if tok is None:
            return generateJsonResponse(success=False, status=400, message="Please provide auth token")
        auth, msg = decode_token(tok)
        if auth == None:
            return generateJsonResponse(success=False, status=401, message=str(msg))

        data = request.get_json()  # Get JSON data from request
        # Check required fields
        #print(data)
        required_fields = ['product_name', 'description', 'price', 'type_jewellery']
        if not all(field in data for field in required_fields):
            return generateJsonResponse(success=False, status=401, message="Missing required fields")
        
        # Call service to create a new product
        return create_product_service(data, auth)
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))


# Route to update an existing product
@product_route.route('/products/update/<product_id>', methods=['PUT'])
def update_product(product_id):
    try:
        tok = request.headers.get('token')
        if tok is None:
            return generateJsonResponse(success=False, status=400, message="Please provide auth token")
        auth, msg = decode_token(tok)
        if auth == None:
            return generateJsonResponse(success=False, status=401, message=str(msg))
        
        data = request.get_json()  # Get JSON data from request
        return update_product_service(product_id, data, auth)  # Call service to update product
        
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))
    

# Route to delete a product
@product_route.route('/products/delete/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        deleted = delete_product_service(product_id)  # Call service to delete product
        if deleted:
            return jsonify({'message': 'Product deleted'}), 200
        else:
            return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
