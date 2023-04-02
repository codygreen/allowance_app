from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from pymongo import MongoClient
import uuid
import os

class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str
    password: str
    type: str
    familyId: str

app = FastAPI()
client = MongoClient(os.environ['MONGO_URI'])
db = client.allowance

@app.get("/", response_model=list[User])
async def show_list():
    collection = db.users
    cursor = collection.find({})
    users = []
    for document in cursor:
        users.append(document)
    return users

@app.post("/", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(user: User):
    collection = db.users
    user = jsonable_encoder(user)
    new_user = collection.insert_one(user)
    created_user = collection.find_one({"_id": new_user.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)