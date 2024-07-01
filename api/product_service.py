from .mongo_connect import DB
from pymongo import MongoClient
from dotenv import dotenv_values
import random
from .mongo_connect import DB

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
        result = DB["Premium"].aggregate(pipeline) 
        # Convert the cursor to a list and return the data
        premium_products_with_details = list(result)
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
        regular_result = DB['Product'].aggregate(pipeline_random)
        regular_products_list = list(regular_result)
        # Shuffle regular products list
        random.shuffle(regular_products_list)
        if len(regular_products_list)>0:
            return {"status": "success","regular_products_list":regular_products_list,"premium_products_list":premium_products_with_details }
        return {"status": "fail", "message": "An error has occured. Please try again!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

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
        result = DB["Premium"].aggregate(pipeline) 
        # Convert the cursor to a list and return the data
        premium_products_with_details = list(result)
        random.shuffle(premium_products_with_details)
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
        regular_result = DB['Product'].aggregate(pipeline_random)
        regular_products_list = list(regular_result)
        # Shuffle regular products list
        random.shuffle(regular_products_list)
        if len(regular_products_list)>0:
            return {"status": "success","categories_products_list":regular_products_list,"categories_premium_products_list":premium_products_with_details }
        return {"status": "fail", "message": "An error has occured. Please try again!"}
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
        result = DB["Premium"].aggregate(pipeline) 
        # Convert the cursor to a list and return the data
        premium_products_with_details = list(result)
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
        regular_result = DB['Product'].aggregate(pipeline_random)
        regular_products_list = list(regular_result)
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
        result = DB["Premium"].aggregate(pipeline) 
        # Convert the cursor to a list and return the data
        premium_products_with_details = list(result)
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
        regular_result = DB['Product'].aggregate(pipeline_random)
        regular_products_list = list(regular_result)
        # Shuffle regular products list
        random.shuffle(regular_products_list)
        if len(regular_products_list)>0:
            return {"status": "success","seller_products_list":regular_products_list,"seller_premium_products_list":premium_products_with_details }
        return {"status": "fail", "message": "An error has occured. Please try again!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
        
def get_seller_products_service(sellerId):
    return {}

def get_searched_products_service(searchInput):
    return {}