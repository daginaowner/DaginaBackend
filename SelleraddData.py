"""
This code is used for seeding Buyer data into the MongoDb database using MongoDB API
"""

import requests

APIKEY = "fIPWHsHbX3Rz22ZL0w10osNJeTehGzb0JWfUyhOn3BkqutjqTSBop4W5jsMChAvy"
ENDPOINT = "https://ap-south-1.aws.data.mongodb-api.com/app/data-quebaek/endpoint/data/v1/action/insertMany"

headers = {
    "apiKey" : APIKEY,
    "Content-Type" : "application/json",
}

# Define the data you want to send in the POST request
data = {
    "dataSource": "DaginaWeb",
    "database": "DaginaDB",
    "collection": "Seller",
    "documents": [
    {
        "email": "martin.king@example.com",
        "password": "sellerpass123",
        "phoneNumber": "123-456-7890",
        "name": "Martin King",
        "address": "101 Elm Street, Springfield, IL, 62701",
        "productLimit": 10,
        "productids": [],
        "listOfCategories": [],
        "noOfProfileVisits": 0
    },
    {
        "email": "susan.lee@example.com",
        "password": "sellerpass123",
        "phoneNumber": "234-567-8901",
        "name": "Susan Lee",
        "address": "202 Cedar Street, Springfield, IL, 62702",
        "productLimit": 10,
        "productids": [],
        "listOfCategories": [],
        "noOfProfileVisits": 0
    },
    {
        "email": "james.taylor@example.com",
        "password": "sellerpass123",
        "phoneNumber": "345-678-9012",
        "name": "James Taylor",
        "address": "303 Birch Street, Springfield, IL, 62703",
        "productLimit": 10,
        "productids": [],
        "listOfCategories": [],
        "noOfProfileVisits": 0
    },
    {
        "email": "emma.brown@example.com",
        "password": "sellerpass123",
        "phoneNumber": "456-789-0123",
        "name": "Emma Brown",
        "address": "404 Ash Street, Springfield, IL, 62704",
        "productLimit": 10,
        "productids": [],
        "listOfCategories": [],
        "noOfProfileVisits": 0
    },
    {
        "email": "david.jones@example.com",
        "password": "sellerpass123",
        "phoneNumber": "567-890-1234",
        "name": "David Jones",
        "address": "505 Walnut Street, Springfield, IL, 62705",
        "productLimit": 10,
        "productids": [],
        "listOfCategories": [],
        "noOfProfileVisits": 0
    }
]
}

# Make the POST request
response = requests.post(url=ENDPOINT, headers=headers, json=data)

# Print the response text
print(response.text)
