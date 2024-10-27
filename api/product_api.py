from flask import Blueprint, request, jsonify
from .product_service import get_products_service,get_products_by_ids_service,get_product_by_id_service, create_product_service, delete_product_service, update_product_service

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

# Route to get multiple products by an array of IDs
@product_route.route('/products', methods=['POST'])
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
    
# Route to add a review to a product
# @product_route.route('/products/<product_id>/add-review/<buyer_id>', methods=['POST'])
# def add_review_to_product(product_id, buyer_id):
#     try:
#         # Parse review data from the request body
#         review_data = request.get_json()

#         # Check if review data is provided
#         if not review_data:
#             return jsonify({'error': 'Review data is required'}), 400

#         # Validate required review fields
#         if 'rating' not in review_data or 'comment' not in review_data:
#             return jsonify({'error': 'Rating and comment are required in the review data'}), 400

#         # Call the service function to add the review
#         updated_product = add_review_to_product_service(product_id, buyer_id, review_data)

#         # Return the updated product with the new review
#         return jsonify(updated_product), 200

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

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
