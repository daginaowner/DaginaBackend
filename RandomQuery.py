"""
This file is used to query db for infomration purposes
"""

"""
This code is used for seeding Buyer data into the MongoDb database using MongoDB API
"""

import requests
import random
import json

APIKEY = "fIPWHsHbX3Rz22ZL0w10osNJeTehGzb0JWfUyhOn3BkqutjqTSBop4W5jsMChAvy"
ENDPOINT = "https://ap-south-1.aws.data.mongodb-api.com/app/data-quebaek/endpoint/data/v1/action/updateOne"

headers = {
    "apiKey" : APIKEY,
    "Content-Type" : "application/json",
}


prod_ids = ['66780f6a953041e0e7ab49b9', '66780f6a953041e0e7ab49ba', '66780f6a953041e0e7ab49bb', '66780f6a953041e0e7ab49bc', '66780f6a953041e0e7ab49bd',
             '66780f6a953041e0e7ab49be', '66780f6a953041e0e7ab49bf', '66780f6a953041e0e7ab49c0', '66780f6a953041e0e7ab49c1', '66780f6a953041e0e7ab49c2', 
             '66780f6a953041e0e7ab49c3', '66780f6a953041e0e7ab49c4', '66780f6a953041e0e7ab49c5', '66780f6a953041e0e7ab49c6', '66780f6a953041e0e7ab49c7', 
             '66780f6a953041e0e7ab49c8', '66780f6a953041e0e7ab49c9', '66780f6a953041e0e7ab49ca', '66780f6a953041e0e7ab49cb', '66780f6a953041e0e7ab49cc']

seller_ids = ['66780a79d24be3e93ef796d0', '66780a79d24be3e93ef796d1', '66780a79d24be3e93ef796d2', '66780a79d24be3e93ef796d3', '66780a79d24be3e93ef796d4']

ind = 0
for i in seller_ids:
    prod5 = prod_ids[ind:ind+5]
    data = {
    "dataSource": "DaginaWeb",
    "database": "DaginaDB",
    "collection": "Seller",
    "filter" : {
        "_id" : {
            "$oid": i,
        }
    },
    "update": {
        "$set": {
            "productids" : prod5
        }
    }
}
    
    response = requests.post(url=ENDPOINT, headers=headers, json=data)
    print(response.text)
    ind += 5
