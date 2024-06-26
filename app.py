import os
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import dotenv_values
from api.user import user_route
app = Flask(__name__)

config = dotenv_values(".env")
mongo_uri = config.get("MONGO_URI")
db_name = config.get("DB_NAME")

client = MongoClient(mongo_uri)
db = client.get_default_database(db_name)

CORS(app)
app.register_blueprint(user_route)

@app.route('/', methods=['GET'])
def hello():
    return 'Hello from server!'

if __name__ == "__main__":
    app.debug = True

    print("Connected to the MongoDB database!")
    app.run(host="0.0.0.0")