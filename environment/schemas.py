from environment.models import duplicate_user, duplicate_email
import time
from passlib.context import CryptContext
from pymongo import MongoClient
from fastapi import HTTPException
import bcrypt
if not hasattr(bcrypt, '__about__'):
    bcrypt.__about__ = type('about', (object,), {'__version__': bcrypt.__version__})
# Initialize bcrypt context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Connect to MongoDB
client = MongoClient("mongodb+srv://tomH:mbWS0uIrROmONBOv@biodevice.3jz8qms.mongodb.net/")
db = client["your_database"]
collection = db["user_accounts"]

collection_list = collection.find().to_list()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def signup():
    #sign up username
    username = input("Create a username: ")
    user_valid = duplicate_user(username)
    #check to see if the username is taken
    while user_valid=="invalid":
        username = input("Username taken. Please choose a different one: ")
        user_valid = duplicate_user(username)

    #sign up email
    email = input("Enter an email: ")
    email_valid = duplicate_email(email)
    #check to see if the email is taken
    while email_valid=="invalid":
        email = input("Email taken. Please choose a different one: ")
        email_valid = duplicate_email(email)


    password = hash_password(input("Create your password: "))

    return [username, email, password]

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def login(email: str, password: str):
    user =collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")
    
    if not verify_password(password, user["password"]):
        raise HTTPException(status_code=403, detail="Invalid password")
    
    return user  # Return the user object for further use

        
        
def input_data():
    while True:
        data = input("input data json: ")
        return data