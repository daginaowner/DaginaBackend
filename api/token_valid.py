import jwt
from dotenv import dotenv_values
from datetime import datetime, timedelta
from flask import request

config = dotenv_values(".env")
secret = config.get("TOKEN_SECRET")

def validate_token():
    try:
        token = request.headers['token']
    except Exception as e:
        return False, "Token not provided"
    try:
        encoded_info = jwt.decode(token, secret, algorithms=["HS256"])
        return True, encoded_info
    except Exception as e:
        return False , "Invalid Token"
    
"""
Sample way to use it
state, info = validate_token()
    if state:
        return func(info, add_params)
    return {"status":"fail", "msg": info}
"""