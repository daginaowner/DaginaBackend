from flask import jsonify
"""
Wrapper function to wrap all responeses as per standard api format
"""
def generateJsonResponse(success, status, message="", data=None):
    return jsonify(
        {
            'success': success,
            'status': status,
            'message': message,
            'data': data,
        }
    )
