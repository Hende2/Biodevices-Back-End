import pymongo
from typing import Dict
from pydantic import ValidationError
from environment.models import data_reading

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://tomH:mbWS0uIrROmONBOv@biodevice.3jz8qms.mongodb.net/")
db = client["your_database"]
collection_accounts = db["user_accounts"]

collection_accounts_list = collection_accounts.find().to_list()

def add_user(details):
    account = {
        "username": details[0],
        "email": details[1],
        "password": details[2],
        "verified": False
    }
    result = collection_accounts.insert_one(account)
    
collection_data = db["user_data"]

collection_data_list = collection_data.find().to_list()
    
def add_reading(details: Dict) -> str:
    try:
        # Validate details against the data_reading schema
        reading = data_reading(**details)
        
        # Convert to dictionary for MongoDB insertion
        reading_dict = reading.dict(by_alias=True)
        
        # Insert into MongoDB
        result = collection_data.insert_one(reading_dict)
        
        return f"Reading added successfully with ID: {result.inserted_id}"
    except ValidationError as e:
        return f"Validation error: {e}"
    except Exception as e:
        return f"An error occurred: {e}"