import pymongo
import uuid
from typing import Optional
from pydantic import BaseModel, Field
from typing import List

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://tomH:mbWS0uIrROmONBOv@biodevice.3jz8qms.mongodb.net/")
db = client["your_database"]
collection = db["user_accounts"]

collection_list = collection.find().to_list()

usernames = [i["username"] for i in collection_list]
emails = [i["email"] for i in collection_list]

users = {"usernames":usernames, "emails":emails}

#checks for duplicate username
def duplicate_user(input_username):
    if input_username in users["usernames"]:
        return "invalid"
    else:
        return "valid"
    
#checks for duplicate email
def duplicate_email(input_email):
    if input_email in users["emails"]:
        return "invalid"
    else:
        return "valid"
    
class DateTimeModel(BaseModel):
    date: int
    time: str

# Models for validation
class ReadingMeasurement(BaseModel):
    name: str
    value: float


class Reading(BaseModel):
    location: dict
    datetime: dict
    measurements: List[ReadingMeasurement]
    isSafe: bool = False
    hasSynced: bool = True
    id: Optional[str] = None
    uid: str


class User(BaseModel):
    uid: str
    email: str
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    uid: Optional[str] = None
