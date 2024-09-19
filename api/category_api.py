from flask import Blueprint, request, jsonify
from .category_service import get_categories_service, create_category_service, delete_category_service, update_category_service,get_category_by_id_service

# Create a blueprint for category routes
category_route = Blueprint('category_route', __name__)

# Route to get details of a specific category by its ID
@category_route.route('/categories/<category_id>', methods=['GET'])
def get_category_by_id(category_id):
    try:
        category = get_category_by_id_service(category_id)  # Call service to fetch category by ID
        if category:
            return jsonify(category), 200
        else:
            return jsonify({'error': 'Category not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Route to get all categories
@category_route.route('/categories', methods=['GET'])
def get_categories():
    try:
        categories = get_categories_service()  # Call service to fetch categories
        return jsonify(categories), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to create a new category
@category_route.route('/categories', methods=['POST'])
def create_category():
    try:
        data = request.get_json()  # Get JSON data from request
        if not data or 'title' not in data or 'description' not in data or 'created_by' not in data:
            return jsonify({'error': 'Category title, description, and created_by are required'}), 400

        # Call service to create a category
        category = create_category_service(
            title=data['title'],
            description=data['description'],
            created_by=data['created_by']
        )
        return jsonify(category), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to update an existing category
@category_route.route('/categories/<category_id>', methods=['PUT'])
def update_category(category_id):
    try:
        data = request.get_json()  # Get JSON data from request
        if not data or 'title' not in data or 'description' not in data:
            return jsonify({'error': 'Category title and description are required'}), 400

        # Call service to update category
        updated_category = update_category_service(
            category_id=category_id,
            title=data['title'],
            description=data['description']
        )

        if updated_category:
            return jsonify(updated_category), 200
        else:
            return jsonify({'error': 'Category not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to delete a category
@category_route.route('/categories/<category_id>', methods=['DELETE'])
def delete_category(category_id):
    try:
        # Call service to delete category
        deleted = delete_category_service(category_id)
        if deleted:
            return jsonify({'message': 'Category deleted'}), 200
        else:
            return jsonify({'error': 'Category not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
