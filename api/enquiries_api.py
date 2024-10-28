from flask import Blueprint, request
from .generateResp import generateJsonResponse
from .enquiries_service import create_enquiry_service, get_enquiry_service, delete_enquiry_service

# Create a blueprint for enquiry routes
enquiries_route = Blueprint('enquiries_route', __name__)

# Create enquiries as they come in
@enquiries_route.route('/enquiries/create', methods=['POST'])
def create_enquiry():
    try:
        data = request.get_json()
        return create_enquiry_service(data)
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))
    
# Get enquiry for particular sellers
@enquiries_route.route('/getenquiries', methods=['POST'])
def get_enquiries():
    try:
        data = request.get_json()
        return get_enquiry_service(data)
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))
    
@enquiries_route.route('/enquiries/delete', methods=['POST'])
def delete_enquiries():
    try:
        data = request.get_json()
        return delete_enquiry_service(data)
    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))