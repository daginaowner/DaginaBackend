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

buyer_ids = ['667809b7794e4d178757017b', '667809b7794e4d178757017c', '667809b7794e4d178757017d', '667809b7794e4d178757017e', '667809b7794e4d178757017f', '667809b7794e4d1787570180', '667809b7794e4d1787570181', '667809b7794e4d1787570182', '667809b7794e4d1787570183', '667809b7794e4d1787570184', '667809b7794e4d1787570185', '667809b7794e4d1787570186', '667809b7794e4d1787570187', '667809b7794e4d1787570188', '667809b7794e4d1787570189', '667809b7794e4d178757018a', '667809b7794e4d178757018b', '667809b7794e4d178757018c', '667809b7794e4d178757018d', '667809b7794e4d178757018e']

# Define the data you want to send in the POST request
data = {
    "dataSource": "DaginaWeb",
    "database": "DaginaDB",
    "collection": "Review",
    "documents": [
  {
    "prod_ref": "",
    "text": "This necklace is absolutely stunning The craftsmanship is top-notch.",
    "owner_id": random.choice(buyer_ids)
  },
  {
    "prod_ref": "",
    "text": "I love this ring It's perfect for everyday wear and makes a great statement piece.",
    "owner_id": random.choice(buyer_ids)
  },
  {
    "prod_ref": "",
    "text": "The earrings are beautiful and well-made. They're a great addition to my collection.",
    "owner_id": random.choice(buyer_ids)
  },
  {
    "prod_ref": "",
    "text": "The bracelet is elegant and fits perfectly. I'm very pleased with my purchase.",
    "owner_id": random.choice(buyer_ids)
  },
  {
    "prod_ref": "",
    "text": "The pendant is exquisite and has a lot of sentimental value. It's a keepsake I'll cherish forever.",
    "owner_id": random.choice(buyer_ids)
  }
]
}

# Make the POST request
response = requests.post(url=ENDPOINT, headers=headers, json=data)

# Print the response text
print(response.text)
