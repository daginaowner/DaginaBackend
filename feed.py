import requests

APIKEY = "fIPWHsHbX3Rz22ZL0w10osNJeTehGzb0JWfUyhOn3BkqutjqTSBop4W5jsMChAvy"
ENDPOINT = "https://ap-south-1.aws.data.mongodb-api.com/app/data-quebaek/endpoint/data/v1/action/aggregate"

headers = {
    "apiKey": APIKEY,
    "Content-Type": "application/json",
}

# Define the aggregation pipeline
pipeline = [
    {
        '$lookup': {
            'from': 'Product', 
            'localField': 'productId', 
            'foreignField': '_id', 
            'as': 'productDetails'
        }
    }, {
        '$unwind': {
            'path': '$productDetails'
        }
    }
]

# Define the data you want to send in the POST request
data = {
    "dataSource": "DaginaWeb",
    "database": "DaginaDB",
    "collection": "Premium",
    "pipeline": pipeline
}

# Make the POST request to aggregate data
response = requests.post(url=ENDPOINT, headers=headers, json=data)

# Print the response text
if response.status_code == 200:
    premium_products_with_details = response.json()["documents"]
    for document in premium_products_with_details:
        print(document)
else:
    print(f"Failed to fetch data: {response.status_code}")
    print(response.text)
