import os
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import dotenv_values

app = Flask(__name__)

config = dotenv_values(".env")
mongo_uri = config.get("MONGO_URI")

client = MongoClient(mongo_uri)
db = client.get_default_database()

CORS(app)

@app.route('/', methods=['GET'])
def hello():
    return 'Hello from server!'

if __name__ == "__main__":
    app.debug = True
    app.mongodb_client = MongoClient(config["MONGO_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")
    app.run(host="0.0.0.0")