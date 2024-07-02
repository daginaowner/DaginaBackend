from .mongo_connect import DB as client
from pymongo import MongoClient
from flask import jsonify
from dotenv import dotenv_values
import random
from bson import ObjectId


def serialize_document(doc):
    """
    Convert ObjectId fields in a document to string.
    """
    if isinstance(doc, dict):
        return {key: serialize_document(value) for key, value in doc.items()}
    elif isinstance(doc, list):
        return [serialize_document(element) for element in doc]
    elif isinstance(doc, ObjectId):
        return str(doc)
    else:
        return doc

def get_products_service():
    try:
        pipeline = [
            {
                '$lookup': {
                    'from': 'Product',  # Ensure the collection name is correct
                    'localField': 'productId',
                    'foreignField': '_id',
                    'as': 'productDetails'
                }
            },
            {
                '$unwind': {
                    'path': '$productDetails'
                }
            },
            {
                '$sample': {
                    'size': 20  # Sample size, adjust as needed
                }
            },
            {
                '$limit': 20  # Limit the number of documents returned
            }
        ]
        # Execute the aggregation pipeline
        result = client["Premium"].aggregate(pipeline)
        # Convert the cursor to a list and return the data
        premium_products_with_details = list(result)
        premium_products_with_details = [serialize_document(doc) for doc in premium_products_with_details]
        random.shuffle(premium_products_with_details)

        premium_count = len(premium_products_with_details)
        max_regular_products = 100 - premium_count

        # Fetch regular products from Product collection
        pipeline_random = [
            {
                '$sample': {
                    'size': max_regular_products  # Sample size of regular products, adjust as needed
                }
            }
        ]
        regular_result = client['Product'].aggregate(pipeline_random)
        regular_products_list = list(regular_result)
        regular_products_list = [serialize_document(doc) for doc in regular_products_list]

        # Shuffle regular products list
        random.shuffle(regular_products_list)
        if len(regular_products_list) > 0:
            return {
                "status": "success",
                "regular_products_list": regular_products_list,
                "premium_products_list": premium_products_with_details
            }
        return {
            "status": "fail",
            "message": "An error has occurred. Please try again!"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }




def get_categories_products_service(category):
        try:
            pipeline = [
                {
                    '$lookup': {
                        'from': 'Product',  # Ensure the collection name is correct
                        'localField': 'productId',
                        'foreignField': '_id',
                        'as': 'productDetails'
                    }
                },
                {
                    '$unwind': {
                        'path': '$productDetails'
                    }
                },
                {
                    '$match': {
                        'productDetails.category': category  # Filter by category
                    }
                },
                {
                    '$sample': {
                        'size': 20  # Sample size, adjust as needed
                    }
                },
                {
                    '$limit': 20  # Limit the number of documents returned
                }
            ]
            # Execute the aggregation pipeline
            result = client["Premium"].aggregate(pipeline) 
            # Convert the cursor to a list and return the data
            premium_products_with_details = list(result)
            random.shuffle(premium_products_with_details)
            premium_products_with_details = [serialize_document(doc) for doc in premium_products_with_details]

            premium_count = len(premium_products_with_details)
            max_regular_products = 100 - premium_count
            
            # Fetch regular products from Product collection
            pipeline_random = [
                {
                    '$match': {
                        'category': category  # Filter by category
                    }
                },
                {
                    '$sample': {
                        'size': max_regular_products  # Sample size of regular products, adjust as needed
                    }
                }
            ]
            regular_result = client['Product'].aggregate(pipeline_random)
            regular_products_list = list(regular_result)
            regular_products_list = [serialize_document(doc) for doc in regular_products_list]
            # Shuffle regular products list
            random.shuffle(regular_products_list)
            
            if len(regular_products_list)>0:
                return {"status": "success","categories_products_list":regular_products_list,"categories_premium_products_list":premium_products_with_details }
            return {"status": "fail", "message": "Category Not Found !! An error has occured. Please try again!"}
        except Exception as e:
            return {"status": "error", "message": str(e)}


def get_price_range_products_service(pricerange):
        try:
            pipeline = [
                {
                    '$lookup': {
                        'from': 'Product',  # Ensure the collection name is correct
                        'localField': 'productId',
                        'foreignField': '_id',
                        'as': 'productDetails'
                    }
                },
                {
                    '$unwind': {
                        'path': '$productDetails'
                    }
                },
                {
                    '$match': {
                        'productDetails.price range': pricerange  # Filter by range
                    }
                },
                {
                    '$sample': {
                        'size': 20  # Sample size, adjust as needed
                    }
                },
                {
                    '$limit': 20  # Limit the number of documents returned
                }
            ]
            # Execute the aggregation pipeline
            result = client["Premium"].aggregate(pipeline) 
            # Convert the cursor to a list and return the data
            premium_products_with_details = list(result)
            premium_products_with_details = [serialize_document(doc) for doc in premium_products_with_details]
            random.shuffle(premium_products_with_details)

            premium_count = len(premium_products_with_details)
            max_regular_products = 100 - premium_count
            
            # Fetch regular products from Product collection
            pipeline_random = [
                {
                    '$match': {
                        'price range': pricerange  # Filter by price range
                    }
                },
                {
                    '$sample': {
                        'size': max_regular_products  # Sample size of regular products, adjust as needed
                    }
                }
            ]
            regular_result = client['Product'].aggregate(pipeline_random)
            regular_products_list = list(regular_result)
            regular_products_list = [serialize_document(doc) for doc in regular_products_list]
            # Shuffle regular products list
            random.shuffle(regular_products_list)
            
            if len(regular_products_list)>0:
                return {"status": "success","categories_products_list":regular_products_list,"categories_premium_products_list":premium_products_with_details }
            return {"status": "fail", "message": "An error has occured. Please try again!"}
        except Exception as e:
            return {"status": "error", "message": str(e)}


def get_seller_products_service(sellerId):
        try:
            pipeline = [
                {
                    '$lookup': {
                        'from': 'Product',  # Ensure the collection name is correct
                        'localField': 'productId',
                        'foreignField': '_id',
                        'as': 'productDetails'
                    }
                },
                {
                    '$unwind': {
                        'path': '$productDetails'
                    }
                },
                {
                    '$match': {
                        'productDetails.seller Id': sellerId  # Filter by range
                    }
                },
                {
                    '$sample': {
                        'size': 20  # Sample size, adjust as needed
                    }
                },
                {
                    '$limit': 20  # Limit the number of documents returned
                }
            ]
            # Execute the aggregation pipeline
            result = client["Premium"].aggregate(pipeline) 
            # Convert the cursor to a list and return the data
            premium_products_with_details = list(result)
            premium_products_with_details = [serialize_document(doc) for doc in premium_products_with_details]
            random.shuffle(premium_products_with_details)

            premium_count = len(premium_products_with_details)
            max_regular_products = 100 - premium_count
            
            # Fetch regular products from Product collection
            pipeline_random = [
                {
                    '$match': {
                        'seller Id': sellerId  # Filter by price range
                    }
                },
                {
                    '$sample': {
                        'size': max_regular_products  # Sample size of regular products, adjust as needed
                    }
                }
            ]
            regular_result = client['Product'].aggregate(pipeline_random)
            regular_products_list = list(regular_result)
            regular_products_list = [serialize_document(doc) for doc in regular_products_list]
            # Shuffle regular products list
            random.shuffle(regular_products_list)
            
            if len(regular_products_list)>0:
                return {"status": "success","seller_products_list":regular_products_list,"seller_premium_products_list":premium_products_with_details }
            return {"status": "fail", "message": "An error has occured. Please try again!"}
        except Exception as e:
            return {"status": "error", "message": str(e)}






def update_no_of_clicks( product_id, no_of_clicks):
    try:
        # Convert product_id to ObjectId
        product_id = ObjectId(product_id)
    except Exception as e:
        return {"error": "Invalid product_id format"}
    
    # Define the query to find the product by product_id
    query = {'_id': product_id}
    
    # Define the update to increment the noOfClicks
    update = {
        '$inc': {
            'noOfClicks': int(no_of_clicks)
        }
    }
    
    # Perform the update
    result = client['Product'].update_one(query, update)
    print(result)
    
    # Check if the update was successful
    if result:
        return {"message": "Product updated successfully."}
    else:
        return {"message": "Product not found."}

def get_clicks_products_service():
        try:
            pipeline = [
                {
                    '$lookup': {
                        'from': 'Product',  # Ensure the collection name is correct
                        'localField': 'productId',
                        'foreignField': '_id',
                        'as': 'productDetails'
                    }
                },
                {
                    '$unwind': {
                        'path': '$productDetails'
                    }
                },
                {
                '$sort': {
                    'productDetails.noOfClicks': -1  # Sort by 'noOfClicks' in descending order
                }
                },
                {
                    '$limit': 20  # Limit the number of documents returned
                }
            ]
            # Execute the aggregation pipeline
            result = client["Premium"].aggregate(pipeline) 
            # Convert the cursor to a list and return the data
            premium_products_with_details = list(result)
            premium_products_with_details = [serialize_document(doc) for doc in premium_products_with_details]

            premium_count = len(premium_products_with_details)
            max_regular_products = 100 - premium_count
            
            # Fetch regular products from Product collection
            pipeline_random = [
                                {
                                    '$sort': {
                                        'noOfClicks': -1
                                    }
                                }, {
                                    '$limit': max_regular_products
                                }
                            ]
            regular_result = client['Product'].aggregate(pipeline_random)
            regular_products_list = list(regular_result)
            regular_products_list = [serialize_document(doc) for doc in regular_products_list]
            
            if len(regular_products_list)>0:
                return {"status": "success","click_sorted_products_list":regular_products_list,"click_sorted_premium_products_list":premium_products_with_details }
            return {"status": "fail", "message": "An error has occured. Please try again!"}
        except Exception as e:
            return {"status": "error", "message": str(e)}  


 