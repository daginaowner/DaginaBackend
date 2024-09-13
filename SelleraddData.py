"""
This code is used for seeding Buyer data into the MongoDb database using MongoDB API
"""

import requests
from dotenv import dotenv_values
import json
import random

config = dotenv_values((".env"))
APIKEY = config.get("APIKEY")
ENDPOINT = "https://ap-south-1.aws.data.mongodb-api.com/app/data-quebaek/endpoint/data/v1/action/insertMany"

user_ids = ["66e487eecd95f03797f9c213","66e487eecd95f03797f9c214","66e487eecd95f03797f9c215","66e487eecd95f03797f9c216","66e487eecd95f03797f9c217","66e487eecd95f03797f9c218","66e487eecd95f03797f9c219","66e487eecd95f03797f9c21a","66e487eecd95f03797f9c21b","66e487eecd95f03797f9c21c"]

headers = {
    "apiKey" : APIKEY,
    "Content-Type" : "application/json",
}

file = open("seller_data.json", 'r')
seller_data = json.load(file)

#For setting ObjectIds in place
for user in seller_data:
    for feedback in user["feedback"]:
        feedback["owner"] = random.choice(user_ids)


# Define the data you want to send in the POST request
data = {
    "dataSource": "DaginaWeb",
    "database": "DaginaDB",
    "collection": "Seller",
    "documents": seller_data
   
}

# Make the POST request
response = requests.post(url=ENDPOINT, headers=headers, json=data)

# Print the response text
print(response.text)