"""
This code is used for seeding Buyer data into the MongoDb database using MongoDB API
"""

import requests
import  random

APIKEY = "fIPWHsHbX3Rz22ZL0w10osNJeTehGzb0JWfUyhOn3BkqutjqTSBop4W5jsMChAvy"
ENDPOINT = "https://ap-south-1.aws.data.mongodb-api.com/app/data-quebaek/endpoint/data/v1/action/insertMany"
seller_ids = ["66780a79d24be3e93ef796d0","66780a79d24be3e93ef796d1","66780a79d24be3e93ef796d2","66780a79d24be3e93ef796d3","66780a79d24be3e93ef796d4"]

headers = {
    "apiKey" : APIKEY,
    "Content-Type" : "application/json",
}

# Define the data you want to send in the POST request
data = {
    "dataSource": "DaginaWeb",
    "database": "DaginaDB",
    "collection": "Product",
    "documents":  [
    {
        "title": "Elegant Gold Necklace",
        "description": "A beautiful and elegant gold necklace perfect for any occasion.",
        "image URLs": [],
        "price range": "₹20000 - ₹25000",
        "reviews": [],
        "category": ["Necklaces"],
        "noOfClicks": 0,
        "enquiry": 0,
        "seller Id": random.choice(seller_ids)
    },
    {
        "title": "Diamond Stud Earrings",
        "description": "Stunning diamond stud earrings that sparkle with every move.",
        "image URLs": [],
        "price range": "₹15000 - ₹20000",
        "reviews": [],
        "category": ["Earrings"],
        "noOfClicks": 0,
        "enquiry": 0,
        "seller Id": random.choice(seller_ids)
    },
    {
        "title": "Silver Charm Bracelet",
        "description": "A delicate silver charm bracelet that adds a touch of elegance.",
        "image URLs": [],
        "price range": "₹5000 - ₹8000",
        "reviews": [],
        "category": ["Bracelets"],
        "noOfClicks": 0,
        "enquiry": 0,
        "seller Id": random.choice(seller_ids)
    },
    {
        "title": "Ruby Pendant Necklace",
        "description": "A striking ruby pendant necklace that captures attention.",
        "image URLs": [],
        "price range": "₹30000 - ₹35000",
        "reviews": [],
        "category": ["Necklaces"],
        "noOfClicks": 0,
        "enquiry": 0,
        "seller Id": random.choice(seller_ids)
    },
    {
        "title": "Gold Hoop Earrings",
        "description": "Classic gold hoop earrings for a timeless look.",
        "image URLs": [],
        "price range": "₹10000 - ₹15000",
        "reviews": [],
        "category": ["Earrings"],
        "noOfClicks": 0,
        "enquiry": 0,
        "seller Id": random.choice(seller_ids)
    },
    {
        "title": "Pearl Strand Necklace",
        "description": "A sophisticated pearl strand necklace for a touch of class.",
        "image URLs": [],
        "price range": "₹18000 - ₹22000",
        "reviews": [],
        "category": ["Necklaces"],
        "noOfClicks": 0,
        "enquiry": 0,
        "seller Id": random.choice(seller_ids)
    },
    {
        "title": "Emerald Drop Earrings",
        "description": "Gorgeous emerald drop earrings that exude luxury.",
        "image URLs": [],
        "price range": "₹25000 - ₹30000",
        "reviews": [],
        "category": ["Earrings"],
        "noOfClicks": 0,
        "enquiry": 0,
        "seller Id": random.choice(seller_ids)
    },
    {
        "title": "Gold Bangle Set",
        "description": "A set of intricately designed gold bangles.",
        "image URLs": [],
        "price range": "₹12000 - ₹16000",
        "reviews": [],
        "category": ["Bracelets"],
        "noOfClicks": 0,
        "enquiry": 0,
        "seller Id": random.choice(seller_ids)
    },
    {
        "title": "Sapphire Ring",
        "description": "An exquisite sapphire ring set in a gold band.",
        "image URLs": [],
        "price range": "₹40000 - ₹45000",
        "reviews": [],
        "category": ["Rings"],
        "noOfClicks": 0,
        "enquiry": 0,
        "seller Id": random.choice(seller_ids)
    },
    {
        "title": "Diamond Tennis Bracelet",
        "description": "A luxurious diamond tennis bracelet for special occasions.",
        "image URLs": [],
        "price range": "₹50000 - ₹60000",
        "reviews": [],
        "category": ["Bracelets"],
        "noOfClicks": 0,
        "enquiry": 0,
        "seller Id": random.choice(seller_ids)
    },
    {
        "title": "Gold Choker Necklace",
        "description": "A trendy gold choker necklace with a modern design.",
        "image URLs": [],
        "price range": "₹15000 - ₹18000",
        "reviews": [],
        "category": ["Necklaces"],
        "noOfClicks": 0,
        "enquiry": 0,
        "seller Id": random.choice(seller_ids)
    },
    {
        "title": "Ruby Stud Earrings",
        "description": "Elegant ruby stud earrings that add a pop of color.",
        "image URLs": [],
        "price range": "₹20000 - ₹25000",
        "reviews": [],
        "category": ["Earrings"],
        "noOfClicks": 0,
        "enquiry": 0,
        "seller Id": random.choice(seller_ids)
    },
    {
        "title": "Silver Cuff Bracelet",
        "description": "A stylish silver cuff bracelet with intricate patterns.",
        "image URLs": [],
        "price range": "₹7000 - ₹10000",
        "reviews": [],
        "category": ["Bracelets"],
        "noOfClicks": 0,
        "enquiry": 0,
        "seller Id": random.choice(seller_ids)
    },
    {
        "title": "Gold Chain Necklace",
        "description": "A simple and elegant gold chain necklace.",
        "image URLs": [],
        "price range": "₹10000 - ₹13000",
        "reviews": [],
        "category": ["Necklaces"],
        "noOfClicks": 0,
        "enquiry": 0,
        "seller Id": random.choice(seller_ids)
    },
    {
        "title": "Pearl Drop Earrings",
        "description": "Beautiful pearl drop earrings that complement any outfit.",
        "image URLs": [],
        "price range": "₹15000 - ₹18000",
        "reviews": [],
        "category": ["Earrings"],
        "noOfClicks": 0,
        "enquiry": 0,
        "seller Id": random.choice(seller_ids)
    },
    {
        "title": "Diamond Engagement Ring",
        "description": "A stunning diamond engagement ring with a classic design.",
        "image URLs": [],
        "price range": "₹60000 - ₹70000",
        "reviews": [],
        "category": ["Rings"],
        "noOfClicks": 0,
        "enquiry": 0,
        "seller Id": random.choice(seller_ids)
    },
    {
        "title": "Emerald Pendant Necklace",
        "description": "A captivating emerald pendant necklace.",
        "image URLs": [],
        "price range": "₹35000 - ₹40000",
        "reviews": [],
        "category": ["Necklaces"],
        "noOfClicks": 0,
        "enquiry": 0,
        "seller Id": random.choice(seller_ids)
    },
    {
        "title": "Gold Stud Earrings",
        "description": "Timeless gold stud earrings for everyday wear.",
        "image URLs": [],
        "price range": "₹8000 - ₹12000",
        "reviews": [],
        "category": ["Earrings"],
        "noOfClicks": 0,
        "enquiry": 0,
        "seller Id": random.choice(seller_ids)
    },
    {
        "title": "Silver Ankle Bracelet",
        "description": "A delicate silver ankle bracelet with charms.",
        "image URLs": [],
        "price range": "₹5000 - ₹7000",
        "reviews": [],
        "category": ["Bracelets"],
        "noOfClicks": 0,
        "enquiry": 0,
        "seller Id": random.choice(seller_ids)
    },
    {
        "title": "Platinum Wedding Band",
        "description": "A sleek platinum wedding band for a lifetime of love.",
        "image URLs": [],
        "price range": "₹50000 - ₹60000",
        "reviews": [],
        "category": ["Rings"],
        "noOfClicks": 0,
        "enquiry": 0,
        "seller Id": random.choice(seller_ids)
    }
]
}

# Make the POST request
response = requests.post(url=ENDPOINT, headers=headers, json=data)

# Print the response text
print(response.text)
