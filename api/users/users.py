from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field
from pymongo import MongoClient
from bson import ObjectId, json_util
import json
import os

app = FastAPI()
client = MongoClient(os.environ['MONGO_URI'])
db = client.allowance

def ObjectIdParser(data):
    resp = json.loads(json_util.dumps(data))
    resp["_id"] = str(resp["_id"]["$oid"])
    return resp
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')

class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    password: str
    type: str
    familyId: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id": "642b03b9f0d9fe0007309f0e",
                "name": "John",
                "password": "1234",
                "type": "guardian",
                "familyId": "642b09500fec1b9fe4ab78ae"
            }
        }

class UpdateUser(BaseModel):
    name: str
    password: str
    type: str
    familyId: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "John",
                "password": "1234",
                "type": "guardian",
                "familyId": "642b09500fec1b9fe4ab78ae"
            }
        }



@app.get("/", response_model=list[User])
async def show_list():
    collection = db.users
    cursor = collection.find({})
    users = []
    for document in cursor:
        users.append(document)
    return users

@app.get("/{id}", response_model=User)
async def show_user(id: str):
    collection = db.users
    user = collection.find_one({"_id": ObjectId(id)})
    return user

@app.post("/", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(user: UpdateUser):
    collection = db.users
    user = jsonable_encoder(user)
    new_user = collection.insert_one(user)
    created_user = collection.find_one({"_id": new_user.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=ObjectIdParser(created_user))

@app.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=User)
async def update_user(id: str, user: UpdateUser):
    collection = db.users
    user = {k: v for k, v in user.dict().items() if v is not None}
    if len(user) >= 1:
        update_result = collection.update_one({"_id": ObjectId(id)}, {"$set": user})
        if update_result.modified_count == 1:
            if update_result.matched_count == 1:
                updated_user = collection.find_one({"_id": ObjectId(id)})
                return updated_user
    if update_result.matched_count == 0:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return Response(status_code=status.HTTP_304_NOT_MODIFIED)

@app.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    collection = db.users
    delete_result = collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(status_code=status.HTTP_404_NOT_FOUND)