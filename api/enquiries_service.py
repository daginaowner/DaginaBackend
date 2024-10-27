from .mongo_connect import DB
from bson import ObjectId
from datetime import datetime
from .generateResp import generateJsonResponse

#Gets the enquiry collection from the database
enquiry_collection = DB["Enquiries"]
buyer_collection = DB["Buyer"]

def create_enquiry_service(data):
    try:
        #Check if all required fields are present
        keys = ["name","phone", "seller_id", "prod_id"]
        for key in keys:
            if key not in data:
                return generateJsonResponse(success=False, status=401, message=f"Please provide {key}")

        resp = enquiry_collection.insert_one({
            "seller_id": ObjectId(str(data["seller_id"])),
            "product_id": ObjectId(str(data["prod_id"])),
            "name": data["name"],
            "phone": data["phone"]
        })
        if resp.inserted_id:
            return generateJsonResponse(success=True, status=201, message="Enquiry made to the seller")
        return generateJsonResponse(success=False, status=401, message="An error occured")
    
    except Exception as e:
         return generateJsonResponse(success=False, status=400, message=str(e))
    
def get_enquiry_service(data):
    try:
        seller_id = str(data["seller_id"])
        print(seller_id)
        result = list(enquiry_collection.find({"seller_id": ObjectId(seller_id)}))
        for i in result:
            i['_id'] = str(i['_id'])
            i['seller_id'] = str(i['seller_id'])
            i['product_id'] = str(i['product_id'])
        return generateJsonResponse(success=True, status=200, message=f"{len(result)} Enquiries found", data={'enquiries': result})
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))
