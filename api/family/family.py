from fastapi import FastAPI, HTTPException, status
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

class Family(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    guardians: list[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id": "642b09500fec1b9fe4ab78ae",
                "name": "Green",
                "guardians": [
                    "642b03b9f0d9fe0007309f0e",
                    "642b050c62d9566c1c02abe5"
                ]
            }
        }

class UpdateFamily(BaseModel):
    name: str
    guardians: list[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Green",
                "guardians": [
                    "642b03b9f0d9fe0007309f0e",
                    "642b050c62d9566c1c02abe5"
                ]
            }
        }



@app.get("/", response_model=list[Family])
async def show_list():
    collection = db.family
    cursor = collection.find({})
    families = []
    for document in cursor:
        families.append(document)
    return families

@app.get("/{id}", response_model=Family)
async def show_family(id: str):
    collection = db.family
    family = collection.find_one({"_id": ObjectId(id)})
    return family

@app.post("/", status_code=status.HTTP_201_CREATED, response_model=Family)
async def create_family(family: UpdateFamily):
    collection = db.family
    family = jsonable_encoder(family)
    new_family = collection.insert_one(family)
    created_family = collection.find_one({"_id": new_family.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=ObjectIdParser(created_family))

@app.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=Family)
async def update_family(id: str, family: UpdateFamily):
    collection = db.family
    family = {k: v for k, v in family.dict().items() if v is not None}
    if len(family) >= 1:
        update_result = collection.update_one({"_id": ObjectId(id)}, {"$set": family})
        if update_result.modified_count == 1:
            if update_result.matched_count == 1:
                updated_family = collection.find_one({"_id": ObjectId(id)})
                return updated_family
    if update_result.matched_count == 0:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return Response(status_code=status.HTTP_304_NOT_MODIFIED)

@app.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_family(id: str):
    collection = db.family
    delete_result = collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(status_code=status.HTTP_404_NOT_FOUND)