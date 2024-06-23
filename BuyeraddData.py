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
    "collection": "Buyer",
    "documents": [
    {
        "email": "john.doe@example.com",
        "password": "password123",
        "phoneNumber": "123-456-7890",
        "name": "John Doe",
        "address": "123 Maple Street, Springfield, IL, 62701"
    },
    {
        "email": "jane.smith@example.com",
        "password": "password123",
        "phoneNumber": "234-567-8901",
        "name": "Jane Smith",
        "address": "456 Oak Street, Springfield, IL, 62702"
    },
    {
        "email": "bob.johnson@example.com",
        "password": "password123",
        "phoneNumber": "345-678-9012",
        "name": "Bob Johnson",
        "address": "789 Pine Street, Springfield, IL, 62703"
    },
    {
        "email": "alice.williams@example.com",
        "password": "password123",
        "phoneNumber": "456-789-0123",
        "name": "Alice Williams",
        "address": "101 Maple Avenue, Springfield, IL, 62704"
    },
    {
        "email": "charles.brown@example.com",
        "password": "password123",
        "phoneNumber": "567-890-1234",
        "name": "Charles Brown",
        "address": "202 Oak Avenue, Springfield, IL, 62705"
    },
    {
        "email": "emily.davis@example.com",
        "password": "password123",
        "phoneNumber": "678-901-2345",
        "name": "Emily Davis",
        "address": "303 Pine Avenue, Springfield, IL, 62706"
    },
    {
        "email": "michael.miller@example.com",
        "password": "password123",
        "phoneNumber": "789-012-3456",
        "name": "Michael Miller",
        "address": "404 Maple Boulevard, Springfield, IL, 62707"
    },
    {
        "email": "sarah.wilson@example.com",
        "password": "password123",
        "phoneNumber": "890-123-4567",
        "name": "Sarah Wilson",
        "address": "505 Oak Boulevard, Springfield, IL, 62708"
    },
    {
        "email": "david.moore@example.com",
        "password": "password123",
        "phoneNumber": "901-234-5678",
        "name": "David Moore",
        "address": "606 Pine Boulevard, Springfield, IL, 62709"
    },
    {
        "email": "laura.taylor@example.com",
        "password": "password123",
        "phoneNumber": "012-345-6789",
        "name": "Laura Taylor",
        "address": "707 Maple Circle, Springfield, IL, 62710"
    },
    {
        "email": "robert.anderson@example.com",
        "password": "password123",
        "phoneNumber": "123-456-7891",
        "name": "Robert Anderson",
        "address": "808 Oak Circle, Springfield, IL, 62711"
    },
    {
        "email": "lisa.thomas@example.com",
        "password": "password123",
        "phoneNumber": "234-567-8902",
        "name": "Lisa Thomas",
        "address": "909 Pine Circle, Springfield, IL, 62712"
    },
    {
        "email": "kevin.jackson@example.com",
        "password": "password123",
        "phoneNumber": "345-678-9013",
        "name": "Kevin Jackson",
        "address": "1010 Maple Drive, Springfield, IL, 62713"
    },
    {
        "email": "nancy.white@example.com",
        "password": "password123",
        "phoneNumber": "456-789-0124",
        "name": "Nancy White",
        "address": "1111 Oak Drive, Springfield, IL, 62714"
    },
    {
        "email": "paul.harris@example.com",
        "password": "password123",
        "phoneNumber": "567-890-1235",
        "name": "Paul Harris",
        "address": "1212 Pine Drive, Springfield, IL, 62715"
    },
    {
        "email": "karen.martin@example.com",
        "password": "password123",
        "phoneNumber": "678-901-2346",
        "name": "Karen Martin",
        "address": "1313 Maple Lane, Springfield, IL, 62716"
    },
    {
        "email": "james.thompson@example.com",
        "password": "password123",
        "phoneNumber": "789-012-3457",
        "name": "James Thompson",
        "address": "1414 Oak Lane, Springfield, IL, 62717"
    },
    {
        "email": "patricia.martinez@example.com",
        "password": "password123",
        "phoneNumber": "890-123-4568",
        "name": "Patricia Martinez",
        "address": "1515 Pine Lane, Springfield, IL, 62718"
    },
    {
        "email": "steven.garcia@example.com",
        "password": "password123",
        "phoneNumber": "901-234-5679",
        "name": "Steven Garcia",
        "address": "1616 Maple Road, Springfield, IL, 62719"
    },
    {
        "email": "barbara.rodriguez@example.com",
        "password": "password123",
        "phoneNumber": "012-345-6790",
        "name": "Barbara Rodriguez",
        "address": "1717 Oak Road, Springfield, IL, 62720"
    }
]
}

# Make the POST request
response = requests.post(url=ENDPOINT, headers=headers, json=data)

# Print the response text
print(response.text)
