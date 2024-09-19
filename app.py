import os
from flask import Flask
from flask_cors import CORS
from api.buyer_api import buyer_route
from api.seller_api import seller_route
from api.product_api import product_route
from api.category_api import category_route
app = Flask(__name__)

CORS(app)
app.register_blueprint(buyer_route)
app.register_blueprint(seller_route)
app.register_blueprint(product_route)
app.register_blueprint(category_route)


@app.route('/', methods=['GET'])
def hello():
    return 'Hello from server!'

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")