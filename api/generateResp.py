from flask import jsonify

"""
Wrapper function to wrap all responses as per standard API format
"""
def generateJsonResponse(success, status, message="", data=None, user_type=None):
    response = {
        'success': success,
        'status': status,
        'message': message,
        'data': data,
    }
    
    # Only add the user_type field if it is provided
    if user_type is not None:
        response['user_type'] = user_type

    return jsonify(response)
