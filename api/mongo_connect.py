from pymongo import MongoClient
from dotenv import dotenv_values

config = dotenv_values(".env")
mongo_uri = config.get("MONGO_URI")
db_name = config.get("DB_NAME")
client = MongoClient(mongo_uri)
DB = client.get_default_database(db_name)

print("Connected to the MongoDB database!")