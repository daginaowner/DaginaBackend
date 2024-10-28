from datetime import datetime
from .mongo_connect import DB
from bson.objectid import ObjectId
from pymongo import ASCENDING, DESCENDING
import json
from flask import jsonify
from .generateResp import generateJsonResponse

# Get the products collection from the database
products_collection = DB.Products
categories_collection = DB.Categories
seller_collection = DB.Seller
buyer_collection = DB.Buyers

from bson import ObjectId
import re

# Allowed fields for updates, excluding fields like `seller_id` that shouldn't be changed
ALLOWED_UPDATE_FIELDS = {
    "product_name", "slug", "images", "description", "is_premium", "price", "discount",
    "resale_value", "type_jewellery", "type_categories", "materials_quantity", "size",
    "extra_details", "hallmark_certificates","likes", "reviews"
}

ALLOWED_KEYS = {
    "product_name", "slug", "images", "description", "is_premium", "price", "discount",
    "resale_value", "type_jewellery",  "materials_quantity", "size",
    "extra_details", "hallmark_certificates"
}

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


# Service to create a new product
def create_product_service(data, auth):
    try:

        #Code for checking whether the request is made by seller
        email = auth['email']
        resp = seller_collection.find_one({"email": str(email)})
        if resp == None:
            return generateJsonResponse(success=False, status=401, message=f"{email} is not a verified Seller")

        validated_data = {key: data[key] for key in data if key in ALLOWED_KEYS}

        # Ensure necessary fields have default values
        validated_data['created_at'] = datetime.utcnow()  # Creation timestamp
        validated_data['clicks'] = 0  # Initialize clicks to 0
        validated_data['likes'] = 0   # Initialize likes to 0
        validated_data['reviews'] = []  # Ensure reviews is an empty list
        validated_data['type_categories'] = []  # Ensure reviews is an empty list
        validated_data['seller_id'] = ObjectId(str(auth['_id']))

        # Convert ObjectId fields where needed
        if 'type_categories' in validated_data:
            validated_data['type_categories'] = [ObjectId(cat) for cat in validated_data['type_categories']]

        # Insert the product into the collection
        result = products_collection.insert_one(validated_data)
        if result.inserted_id:
            return generateJsonResponse(success=True, status=200, message="Object added to the seller", data={'prod_id': str(result.inserted_id)})
        return generateJsonResponse(success=False, status=400, message="Error Adding Product!")

    except Exception as e:
        raise Exception(f"Error creating product: {str(e)}")


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


def update_product_service(product_id, data, auth):
    try:
        # Code for validating seller token by matching sellerid of the product
        tok_id = auth['_id']
        resp = products_collection.find_one({'_id': ObjectId(str(product_id))}, {'seller_id':1})
        if resp == None:
            return generateJsonResponse(success=False, status=401, message=f"Cannot found the product with id {product_id}")

        if str(tok_id) != str(resp['seller_id']):
            return generateJsonResponse(success=False, status=400, message=f"{auth['email']} is not the owner of the product {product_id}")

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
        if result.matched_count > 0:
            if result.upserted_id:
                product_id = str(result.upserted_id)
            return generateJsonResponse(success=True, status=200, message=f"Product details edited successfully", data={'product_id': str(product_id)})
        else:
            return generateJsonResponse(success=False, status=400, message=f"Product not found")

    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))


def delete_product_service(product_id):
    try:
        result = products_collection.delete_one({"_id": ObjectId(product_id)})  # Delete product by ID
        if result.deleted_count > 0:
            return True
        else:
            return False
    except Exception as e:
        raise Exception(f"Error deleting product: {str(e)}")
