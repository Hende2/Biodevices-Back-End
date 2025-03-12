import pymongo
# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://tomH:mbWS0uIrROmONBOv@biodevice.3jz8qms.mongodb.net/")
db = client["Firebase"]
collection = db["Firebase_data"]

measurements = [
        {
            # [string length: variable]
            "name": "chloride",
            #[array of floats length: variable]
            "values": [
                0,
                0,
                0,
                0,
                0
            ]
        },
        {
            # [string length: variable]
            "name": "ph",
            # [array of floats length: variable]
            "values": [
                0,
                0,
                0,
                0,
                0
            ]
        },
        {
            # [string length: variable]
            "name": "temperature",
            # [array of floats length: variable]
            "values": [
                0,
                0,
                0,
                0,
                0
            ]
        },
        {
            # [string length: variable]
            "name": "turbidity",
            # [array of floats length: variable]
            "values": [
                0,
                0,
                0,
                0,
                0
            ]
        }
        # etc...
    ]

test1 = {
    'uid': 'Test_1'
}

def add_single_dp(item):
    collection.insert_one(item)

add_single_dp(test1)