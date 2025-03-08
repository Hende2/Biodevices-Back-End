from fastapi import FastAPI, HTTPException,Depends, Body
from environment.schemas import signup,login,input_data
from dotenv import dotenv_values
from pymongo import MongoClient
from environment.config import add_user,add_reading

#config
config = dotenv_values(".env")
#create app
app = FastAPI()

#endpoint for registering
@app.post("/register")
def register_user():
    details = signup()
    add_user(details)
    return {"message": "user registered"}

#base
@app.get("/")
async def root():
    return {"message": "home"}

#endpoint for adding a reading
@app.post("/uploadreading")
def upload_reading(
    email: str = Body(..., embed=True),
    password: str = Body(..., embed=True),
    data: dict = Body(..., embed=True)
):
    # Verify user credentials
    user = login(email=email, password=password)
    
    # Add reading
    add_reading(data)
    
    return {"message": "Data uploaded successfully"}
