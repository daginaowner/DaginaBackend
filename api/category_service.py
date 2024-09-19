from datetime import datetime
from .mongo_connect import DB
from bson.objectid import ObjectId

# Get the categories collection from the database
categories_collection = DB.Categories


# Service to get a category by its ID
def get_category_by_id_service(category_id):
    try:
        category = categories_collection.find_one({"_id": ObjectId(category_id)})  # Find category by ID
        if category:
            category['_id'] = str(category['_id'])  # Convert ObjectId to string for JSON
            category['created_by'] = str(category['created_by'])  # Convert created_by ObjectId to string
            return category
        else:
            return None  # Return None if no category is found
    except Exception as e:
        raise Exception(f"Error fetching category by ID: {str(e)}")
    
# Service to get all categories
def get_categories_service():
    try:
        categories = list(categories_collection.find())  # Fetch all documents in the collection
        for category in categories:
            category['_id'] = str(category['_id'])  # Convert ObjectId to string for easier JSON serialization
            category['created_by'] = str(category['created_by'])
        return categories
    except Exception as e:
        raise Exception(f"Error fetching categories: {str(e)}")

# Service to create a new category
def create_category_service(title, description, created_by):
    try:
        # Prepare category document
        category = {
            "title": title,
            "slug": title.lower().replace(" ", "_"),  # Generate slug from title
            "description": description,
            "created_by": ObjectId(created_by),  # Convert to ObjectId
            "timestamp": datetime.utcnow()
        }
        result = categories_collection.insert_one(category)  # Insert category into collection
        category['_id'] = str(result.inserted_id)  # Return the inserted ID as a string
        category['created_by'] = str(category['created_by'])  # Convert ObjectId to string
        return category
    except Exception as e:
        raise Exception(f"Error creating category: {str(e)}")

# Service to update an existing category
def update_category_service(category_id, title, description):
    try:
        category = categories_collection.find_one({"_id": ObjectId(category_id)})  # Find category by ID
        if not category:
            return None

        # Update the category fields
        update_fields = {
            "title": title,
            "slug": title.lower().replace(" ", "_"),  # Update slug
            "description": description,
            "timestamp": datetime.utcnow()  # Update timestamp
        }

        # Perform the update
        categories_collection.update_one({"_id": ObjectId(category_id)}, {"$set": update_fields})

        # Fetch the updated document and return it
        updated_category = categories_collection.find_one({"_id": ObjectId(category_id)})
        updated_category['_id'] = str(updated_category['_id'])  # Convert ObjectId to string
        updated_category['created_by'] = str(updated_category['created_by'])  # Convert ObjectId to string
        return updated_category
    except Exception as e:
        raise Exception(f"Error updating category: {str(e)}")

# Service to delete a category
def delete_category_service(category_id):
    try:
        # Find and delete the category by ID
        result = categories_collection.delete_one({"_id": ObjectId(category_id)})
        return result.deleted_count > 0  # Return True if deletion was successful
    except Exception as e:
        raise Exception(f"Error deleting category: {str(e)}")
