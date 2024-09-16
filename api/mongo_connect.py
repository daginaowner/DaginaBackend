from pymongo import MongoClient
from dotenv import dotenv_values

config = dotenv_values(".env")
mongo_uri = config.get("MONGO_URI")
db_name = config.get("DB_NAME")
client = MongoClient(mongo_uri)
DB = None

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    DB = client.get_default_database(db_name)
    print("Connected to the Dagina database!")
    
except Exception as e:
    print(f"An error occured while connecting \n{e}")
