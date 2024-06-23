"""
This code is used for seeding Buyer data into the MongoDb database using MongoDB API
"""

import requests
import random

APIKEY = "fIPWHsHbX3Rz22ZL0w10osNJeTehGzb0JWfUyhOn3BkqutjqTSBop4W5jsMChAvy"
ENDPOINT = "https://ap-south-1.aws.data.mongodb-api.com/app/data-quebaek/endpoint/data/v1/action/insertMany"

headers = {
    "apiKey" : APIKEY,
    "Content-Type" : "application/json",
}

seller_ids = [""]

# Define the data you want to send in the POST request
data = {
    "dataSource": "DaginaWeb",
    "database": "DaginaDB",
    "collection": "Category",
    "documents": [
    {
        "categoryName": "Necklaces",
        "description": "Elegant necklaces made from various precious metals and gemstones.",
        "productIds": [],
        "ownerId": random.choice(seller_ids)
    },
    {
        "categoryName": "Earrings",
        "description": "A variety of beautiful earrings including studs, hoops, and drops.",
        "productIds": [],
        "ownerId": random.choice(seller_ids)
    },
    {
        "categoryName": "Bracelets",
        "description": "Stylish bracelets available in different designs and materials.",
        "productIds": [],
        "ownerId": random.choice(seller_ids)
    },
    {
        "categoryName": "Rings",
        "description": "Exquisite rings suitable for engagements, weddings, and everyday wear.",
        "productIds": [],
        "ownerId": random.choice(seller_ids)
    },
    {
        "categoryName": "Anklets",
        "description": "Delicate anklets crafted from high-quality materials.",
        "productIds": [],
        "ownerId": random.choice(seller_ids)
    }
]

}

# Make the POST request
response = requests.post(url=ENDPOINT, headers=headers, json=data)

# Print the response text
print(response.text)
