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

# Service to create a new product
def create_product_service(data):
    try:
        #print(data)
        data['created_at'] = datetime.utcnow()  # Add creation timestamp
        # Ensure that ObjectId fields are converted to the appropriate format
        if 'type_categories' in data:
            data['type_categories'] = [ObjectId(cat) for cat in data['type_categories']]  # Convert category IDs to ObjectId
        if 'seller_id' in data:
            data['seller_id'] = ObjectId(data['seller_id'])  # Convert seller_id to ObjectId
        if 'reviews' in data:
            # Iterate through each review
            for review in data['reviews']:
                # Convert 'ratedby' field to ObjectId if it exists
                if 'ratedby' in review:
                    review['ratedby'] = ObjectId(review['ratedby'])

        result = products_collection.insert_one(data)  # Insert new product
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

# Service to update an existing product
def update_product_service(product_id, data):
    try:
        if 'title' in data:
            data['slug'] = generate_slug(data['title'])
        if 'type_categories' in data:
            data['type_categories'] = [ObjectId(cat) for cat in data['type_categories']]  # Convert category IDs to ObjectId
        if 'reviews' in data:
            data['reviews'] = [ObjectId(review) for review in data['reviews']]
        if 'seller_id' in data:
            data['seller_id'] = ObjectId(data['seller_id'])  # Convert seller_id to ObjectId
        data['updated_at'] = datetime.utcnow()  # Add update timestamp

        result = products_collection.update_one({"_id": ObjectId(product_id)}, {"$set": data})  # Update the product
        if result.modified_count > 0:
            updated_product = products_collection.find_one({"_id": ObjectId(product_id)})
            updated_product['_id'] = str(updated_product['_id'])  # Convert ObjectId to string
            updated_product['seller_id'] = str(updated_product['seller_id'])  # Convert seller_id ObjectId to string
            updated_product['type_categories'] = [str(cat) for cat in updated_product['type_categories']]  # Convert categories ObjectId to string
        if 'reviews' in updated_product:
            for review in updated_product['reviews']:
                # Convert 'ratedby' field to ObjectId if it exists
                if 'ratedby' in review:
                    review['ratedby'] = str(review['ratedby'])            
            return updated_product
        else:
            return None
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
