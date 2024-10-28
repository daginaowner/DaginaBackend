from datetime import datetime
from .mongo_connect import DB
from bson.objectid import ObjectId
from pymongo import ASCENDING, DESCENDING
import json
from flask import jsonify
# Get the products collection from the database
products_collection = DB.Products
categories_collection = DB.Categories
seller_collection = DB.Sellers
buyer_collection = DB.Buyers

from bson import ObjectId
import re

def generate_slug(title):
    # Convert title to lowercase, remove non-alphanumeric characters, and replace spaces with hyphens
    slug = re.sub(r'[^a-zA-Z0-9\s-]', '', title).strip().lower()
    slug = re.sub(r'\s+', '-', slug)
    return slug

def get_products_service(query_params):
    try:
        # Base query to filter products
        exclude_fields = ["page", "sort", "limit", "fields"]
        query_obj = {k: v for k, v in query_params.items() if k not in exclude_fields}
        
                # Handle comparison operators manually
        query = {}
        for key, value in query_obj.items():
            if '__gte' in key:
                query[key.replace('__gte', '')] = {'$gte': float(value)}
            elif '__gt' in key:
                query[key.replace('__gt', '')] = {'$gt': float(value)}
            elif '__lte' in key:
                query[key.replace('__lte', '')] = {'$lte': float(value)}
            elif '__lt' in key:
                query[key.replace('__lt', '')] = {'$lt': float(value)}
            else:
                query[key] = value  # Normal fields
        
            if 'seller_id' in query_params:
                try:
                    query['seller_id'] = ObjectId(query_params['seller_id'])  # Convert to ObjectId
                except Exception:
                    raise ValueError("Invalid seller_id format")

        print(f"MongoDB Query: {query}")  # Debugging

        # Initialize the MongoDB query
        mongo_query = products_collection.find(query)

        # Sorting
        sort_by = query_params.get('sort')
        if sort_by:
            sort_criteria = [(field.strip(), ASCENDING if not field.startswith('-') else DESCENDING)
                             for field in sort_by.split(',')]
            mongo_query = mongo_query.sort(sort_criteria)
        else:
            mongo_query = mongo_query.sort([("createdAt", DESCENDING)])  # Default sorting by creation date

        # Field limiting
        fields = query_params.get('fields')
        if fields:
            field_projection = {field: 1 for field in fields.split(',')}
            print(f"Field Projection: {field_projection}")  # Debugging
            mongo_query = mongo_query.project(field_projection)  # Use correct method

        # Pagination
        page = int(query_params.get('page', 1))
        limit = int(query_params.get('limit', 10))
        skip = (page - 1) * limit
        mongo_query = mongo_query.skip(skip).limit(limit)

        # Check if the requested page exists
        if 'page' in query_params:
            product_count = products_collection.count_documents({})
            if skip >= product_count:
                return jsonify({"error": "This page does not exist"}), 400

        # Fetch products
        products = list(mongo_query)
        # Convert ObjectId fields to strings
        for product in products:
            product['_id'] = str(product['_id'])
            if 'seller_id' in product:
                product['seller_id'] = str(product['seller_id'])
            if 'type_categories' in product:
                product['type_categories'] = [str(cat) for cat in product['type_categories']]
            if 'reviews' in product:
                for review in product['reviews']:
                    # Convert 'ratedby' field to ObjectId if it exists
                    if 'ratedby' in review:
                        review['ratedby'] = str(review['ratedby'])

        return products

    except Exception as e:
        raise Exception(f"Error fetching products: {str(e)}")

# Service to get a product by its ID
def get_product_by_id_service(product_id):
    try:
        product = products_collection.find_one({"_id": ObjectId(product_id)})  # Find product by ID
        if product:
            product['_id'] = str(product['_id'])  # Convert ObjectId to string
            seller = seller_collection.find_one({"_id": ObjectId(product['seller_id'])})
            if seller:
                product['seller'] = {
                    '_id': str(seller['_id']),
                    'name': seller.get('name'),  # Include necessary seller details
                    'email': seller.get('email'),
                }
            else:
                product['seller'] = None
            # Remove 'seller_id' after populating
            product.pop('seller_id', None)
            categories = categories_collection.find({"_id": {"$in": [ObjectId(cat_id) for cat_id in product['type_categories']]}})
            product['categories'] = [{'id': str(cat['_id']), 'title': cat.get('title'),'description':cat.get("description")} for cat in categories]
            product.pop('type_categories', None)
            if 'reviews' in product:
                for review in product['reviews']:
                    # Convert 'ratedby' field to ObjectId if it exists
                    if 'ratedby' in review:
                        review['ratedby'] = str(review['ratedby'])


            return product
        else:
            return None
    except Exception as e:
        raise Exception(f"Error fetching product by ID: {str(e)}")

# Service to get products by their IDs
def get_products_by_ids_service(product_ids):
    try:
        # Convert string IDs to ObjectId instances
        object_ids = [ObjectId(product_id) for product_id in product_ids]
        
        # Find all products that match any of the IDs in `object_ids`
        products = products_collection.find({"_id": {"$in": object_ids}})
        
        result = []
        
        # Process each product in the result set
        for product in products:
            # Convert ObjectId to string for the response
            product['_id'] = str(product['_id'])
            
            # Fetch and embed seller details
            seller = seller_collection.find_one({"_id": ObjectId(product['seller_id'])})
            if seller:
                product['seller'] = {
                    '_id': str(seller['_id']),
                    'name': seller.get('name'),
                    'email': seller.get('email'),
                }
            else:
                product['seller'] = None
            
            # Remove 'seller_id' field
            product.pop('seller_id', None)
            
            # Fetch and embed categories details
            categories = categories_collection.find({"_id": {"$in": [ObjectId(cat_id) for cat_id in product.get('type_categories', [])]}})
            product['categories'] = [{'id': str(cat['_id']), 'title': cat.get('title'), 'description': cat.get("description")} for cat in categories]
            
            # Remove 'type_categories' field
            product.pop('type_categories', None)
            
            # Convert 'ratedby' in reviews to string if it exists
            if 'reviews' in product:
                for review in product['reviews']:
                    if 'ratedby' in review:
                        review['ratedby'] = str(review['ratedby'])
            
            result.append(product)
        
        return result
    
    except Exception as e:
        raise Exception(f"Error fetching products by IDs: {str(e)}")

ALLOWED_KEYS = {
    "product_name", "slug", "images", "description", "is_premium", "price", "discount",
    "resale_value", "type_jewellery",  "materials_quantity", "size",
    "extra_details", "hallmark_certificates", "seller_id"
}
# Service to create a new product
def create_product_service(data):
    try:
        validated_data = {key: data[key] for key in data if key in ALLOWED_KEYS}

        # Ensure necessary fields have default values
        validated_data['created_at'] = datetime.utcnow()  # Creation timestamp
        validated_data['clicks'] = 0  # Initialize clicks to 0
        validated_data['likes'] = 0   # Initialize likes to 0
        validated_data['reviews'] = []  # Ensure reviews is an empty list
        validated_data['type_categories'] = []  # Ensure reviews is an empty list

        # Convert ObjectId fields where needed
        if 'type_categories' in validated_data:
            validated_data['type_categories'] = [ObjectId(cat) for cat in validated_data['type_categories']]
        if 'seller_id' in validated_data:
            validated_data['seller_id'] = ObjectId(validated_data['seller_id'])

        # Insert the product into the collection
        result = products_collection.insert_one(validated_data)
        new_product = products_collection.find_one({"_id": result.inserted_id})
        new_product['_id'] = str(new_product['_id'])  # Convert ObjectId to string
        new_product['seller_id'] = str(new_product['seller_id'])  # Convert seller_id ObjectId to string
        new_product['type_categories'] = [str(cat) for cat in new_product['type_categories']]  # Convert categories ObjectId to string
        if 'reviews' in new_product:
            for review in new_product['reviews']:
                # Convert 'ratedby' field to ObjectId if it exists
                if 'ratedby' in review:
                    review['ratedby'] = str(review['ratedby'])

        return new_product
    except Exception as e:
        raise Exception(f"Error creating product: {str(e)}")

# Allowed fields for updates, excluding fields like `seller_id` that shouldn't be changed
ALLOWED_UPDATE_FIELDS = {
    "product_name", "slug", "images", "description", "is_premium", "price", "discount",
    "resale_value", "type_jewellery", "type_categories", "materials_quantity", "size",
    "extra_details", "hallmark_certificates","likes", "reviews"
}

def validate_product_data(data):
    errors = []
    
    # Validate numeric fields
    if 'price' in data and not isinstance(data['price'], (int, float)):
        errors.append("Price must be a numeric value.")
    if 'discount' in data and (not isinstance(data['discount'], int) or not (0 <= data['discount'] <= 100)):
        errors.append("Discount must be an integer between 0 and 100.")
    if 'likes' in data and not isinstance(data['likes'], int):
        errors.append("Likes must be an integer.")

    # Validate fields with specific structure
    if 'type_categories' in data:
        if not isinstance(data['type_categories'], list) or not all(isinstance(cat, str) for cat in data['type_categories']):
            errors.append("Type categories must be a list of strings.")
    if 'reviews' in data:
        if not isinstance(data['reviews'], list) or not all(isinstance(review, dict) for review in data['reviews']):
            errors.append("Reviews must be a list of dictionaries.")

    # Validate structure of nested fields if they are present
    if 'materials_quantity' in data and not isinstance(data['materials_quantity'], dict):
        errors.append("Materials quantity must be a dictionary.")
    if 'size' in data and not isinstance(data['size'], dict):
        errors.append("Size must be a dictionary.")
    
    return errors
def update_product_service(product_id, data):
    try:
        # Filter out any fields that are not allowed
        data = {key: value for key, value in data.items() if key in ALLOWED_UPDATE_FIELDS}
        
        # Validate the input data
        validation_errors = validate_product_data(data)
        if validation_errors:
            return {"error": validation_errors}, 400
        
        # Special handling for slug if 'product_name' is updated
        if 'product_name' in data:
            data['slug'] = generate_slug(data['product_name'])
        
        # Convert specific fields to ObjectId where necessary
        if 'type_categories' in data:
            data['type_categories'] = [ObjectId(cat) for cat in data['type_categories']]
        
        # Convert reviews to include ObjectId for 'ratedby' field if provided
        if 'reviews' in data:
            for review in data['reviews']:
                if 'ratedby' in review:
                    review['ratedby'] = ObjectId(review['ratedby'])
        
        # Add an update timestamp
        data['updated_at'] = datetime.utcnow()

        # Update the product in the database
        result = products_collection.update_one({"_id": ObjectId(product_id)}, {"$set": data})
        
        # Check if the update was successful
        if result.modified_count > 0:
            # Retrieve and format the updated product
            updated_product = products_collection.find_one({"_id": ObjectId(product_id)})
            updated_product['_id'] = str(updated_product['_id'])
            updated_product['seller_id'] = str(updated_product['seller_id'])  # Convert seller_id ObjectId to string
            updated_product['type_categories'] = [str(cat) for cat in updated_product['type_categories']]
            
            # Convert ObjectId fields in reviews if present
            if 'reviews' in updated_product:
                for review in updated_product['reviews']:
                    if 'ratedby' in review:
                        review['ratedby'] = str(review['ratedby'])

            return updated_product, 200
        else:
            return {"error": "Product not found or no changes made."}, 404
    except Exception as e:
        raise Exception(f"Error updating product: {str(e)}")


# def add_review_to_product_service(product_id, buyer_id, review_data):
#     try:
#         # Convert product_id and buyer_id to ObjectId
#         product_id = ObjectId(product_id)
#         buyer_id = ObjectId(buyer_id)

#         # Validate that the product exists
#         product = products_collection.find_one({"_id": product_id})
#         if not product:
#             raise Exception("Product not found")

#         # Validate that the buyer exists (assuming there’s a buyers_collection)
#         buyer = buyer_collection.find_one({"_id": buyer_id})
#         if not buyer:
#             raise Exception("Buyer not found")

#         # Append the buyer's ID to the review data
#         review_data['ratedby'] = buyer_id
#         review_data['created_at'] = datetime.utcnow()  # Add timestamp to the review

#         # Update the product by appending the new review
#         result = products_collection.update_one(
#             {"_id": product_id},
#             {"$push": {"reviews": review_data}}
#         )

#         if result.modified_count > 0:
#             # Return the updated product with the new review
#             updated_product = products_collection.find_one({"_id": product_id})
#             updated_product['_id'] = str(updated_product['_id'])
#             updated_product['seller_id'] = str(updated_product['seller_id'])
#             updated_product['type_categories'] = [str(cat) for cat in updated_product['type_categories']]
#             for review in updated_product.get('reviews', []):
#                 review['ratedby'] = str(review['ratedby'])
#             return updated_product
#         else:
#             raise Exception("Failed to add review to the product")

#     except Exception as e:
#         raise Exception(f"Error adding review to product: {str(e)}")

# Service to delete a product by its ID
def delete_product_service(product_id):
    try:
        result = products_collection.delete_one({"_id": ObjectId(product_id)})  # Delete product by ID
        if result.deleted_count > 0:
            return True
        else:
            return False
    except Exception as e:
        raise Exception(f"Error deleting product: {str(e)}")
