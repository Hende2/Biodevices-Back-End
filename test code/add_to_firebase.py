from pymongo_get_database import get_database
dbname = get_database()
collection_name = dbname['Firebase_data']
print("Hi")
print(collection_name)
# from pymongo import MongoClient
# connection_string = "mongodb+srv://tomH:mbWS0uIrROmONBOv@biodevice.3jz8qms.mongodb.net/"
# client = MongoClient(connection_string)
# collection = client['Firebase_data']

point = {
    'uid': 12e21333
}

def insert_data(data):
    collection_name.insert_one(data)
    return "Complete"

insert_data(point)