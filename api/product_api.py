from flask import Blueprint, request, jsonify
from .product_service import get_products_service, get_product_by_id_service, create_product_service, delete_product_service, update_product_service

# Create a blueprint for product routes
product_route = Blueprint('product_route', __name__)

@product_route.route('/products', methods=['GET'])
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
@product_route.route('/products/<product_id>', methods=['GET'])
def get_product_by_id(product_id):
    try:
        product = get_product_by_id_service(product_id)  # Call service to fetch product by ID
        if product:
            return jsonify(product), 200
        else:
            return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to create a new product
@product_route.route('/products', methods=['POST'])
def create_product():
    try:
        data = request.get_json()  # Get JSON data from request
        # Check required fields
        required_fields = ['product_name', 'description', 'price', 'type_jewellery', 'seller_id']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Call service to create a new product
        product = create_product_service(data)
        return jsonify(product), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to update an existing product
@product_route.route('/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    try:
        data = request.get_json()  # Get JSON data from request
        updated_product = update_product_service(product_id, data)  # Call service to update product
        if updated_product:
            return jsonify(updated_product), 200
        else:
            return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to delete a product
@product_route.route('/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        deleted = delete_product_service(product_id)  # Call service to delete product
        if deleted:
            return jsonify({'message': 'Product deleted'}), 200
        else:
            return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
