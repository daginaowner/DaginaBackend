import os
from flask import Flask
from flask_cors import CORS
from api.user_api import user_route
app = Flask(__name__)

CORS(app)
app.register_blueprint(user_route)

@app.route('/', methods=['GET'])
def hello():
    return 'Hello from server!'

if __name__ == "__main__":
    app.debug = True

    print("Connected to the MongoDB database!")
    app.run(host="0.0.0.0")