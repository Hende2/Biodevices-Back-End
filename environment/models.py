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

class Measurement(BaseModel):
    name: str
    values: List[int]

class Location(BaseModel):
    latitude: float
    longitude: float

class data_reading(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    datetime: DateTimeModel
    hasSynced: bool
    isSafe: bool
    location: Location
    measurements: List[Measurement]
    timeIntervals: List[int]
    uid: str  
    
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "2IadT7MIyb04MiNS5oZ10",
                "datetime": {
                    "date": 12093600,
                    "time": "31:05:23"
                },
                "hasSynced": True,
                "isSafe": False,
                "location": {
                    "latitude": 0.0,
                    "longitude": 0.0
                },
                "measurements": [
                    {
                        "name": "chloride",
                        "values": [
                            0,
                            0,
                            0,
                            0,
                            0
                        ]
                    },
                    {
                        "name": "ph",
                        "values": [
                            0,
                            0,
                            0,
                            0,
                            0
                        ]
                    },
                    {
                        "name": "temperature",
                        "values": [
                            0,
                            0,
                            0,
                            0,
                            0
                        ]
                    },
                    {
                        "name": "turbidity",
                        "values": [
                            0,
                            0,
                            0,
                            0,
                            0
                        ]
                    }
                ],
                "timeIntervals": [
                    0,
                    100,
                    200,
                    300,
                    400
                ],
                "uid": "Gclcb3xyWyQw4AD82WuaEGxbE5E2"
            }
        }
