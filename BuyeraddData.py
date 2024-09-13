"""
This code is used for seeding Buyer data into the MongoDb database using MongoDB API
"""

import requests
from dotenv import dotenv_values
import json

config = dotenv_values(".env")
ENDPOINT = "https://ap-south-1.aws.data.mongodb-api.com/app/data-quebaek/endpoint/data/v1/action/insertMany"
APIKEY = config.get("APIKEY")

headers = {
    "apiKey" : APIKEY,
    "Content-Type" : "application/json",
}

file = open('buyer_data.json', 'r')
user_data = json.load(file)

# Define the data you want to send in the POST request
data = {
    "dataSource": "DaginaWeb",
    "database": "DaginaDB",
    "collection": "Buyer",
    "documents": user_data
}

# Make the POST request
response = requests.post(url=ENDPOINT, headers=headers, json=data)

# Print the response text
print(response.text)
