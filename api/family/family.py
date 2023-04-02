from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from pymongo import MongoClient
import settings
import uuid

class Family(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str
    guardians: list[int]

app = FastAPI()
client = MongoClient(settings.MONGO_URI)
db = client.allowance

@app.get("/", response_model=list[Family])
async def show_list():
    collection = db.family
    cursor = collection.find({})
    families = []
    for document in cursor:
        families.append(document)
    return families

@app.post("/", status_code=status.HTTP_201_CREATED, response_model=Family)
async def create_family(family: Family):
    collection = db.family
    family = jsonable_encoder(family)
    new_family = collection.insert_one(family)
    created_family = collection.find_one({"_id": new_family.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_family)