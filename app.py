import os
from flask import Flask
from flask_cors import CORS
from api.buyer_api import buyer_route
from api.seller_api import seller_route
from api.product_api import product_route
from api.category_api import category_route
from flask import request
from api.buyerService import buyer_login_service
from api.sellerService import seller_login_service
from api.generateResp import generateJsonResponse
app = Flask(__name__)

CORS(app)
app.register_blueprint(buyer_route)
app.register_blueprint(seller_route)
app.register_blueprint(product_route)
app.register_blueprint(category_route)


@app.route('/', methods=['GET'])
def hello():
    return 'Hello from server!'

# common login 
@app.route("/login", methods=['POST'])
def login():
    try:
        data = request.get_json()

        # Attempt buyer login first
        buyer_response = buyer_login_service(data)
        if buyer_response.get_json().get("success", False):  # Check if buyer login was successful
            # Add a "user_type" flag to indicate this is a buyer response
            return generateJsonResponse(success=True, status=200, data=buyer_response.get_json().get("data"), user_type="buyer")

        # Attempt seller login if buyer login fails
        seller_response = seller_login_service(data)
        if seller_response.get_json().get("success", False):  # Check if seller login was successful
            # Add a "user_type" flag to indicate this is a seller response
            return generateJsonResponse(success=True, status=200, data=seller_response.get_json().get("data"), user_type="seller")

        # If neither login is successful, return a generic failure response
        return generateJsonResponse(success=False, status=401, message="Invalid credentials for both buyer and seller.")

    except Exception as e:
        return generateJsonResponse(success=False, status=400, message=str(e))


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")