from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from pymongo import MongoClient
import uuid
import sys

sys.path.append("..")

import settings

class Ledger(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    userId: str
    amount: int
    type: str

app = FastAPI()
client = MongoClient(settings.MONGO_URI)
db = client.allowance

@app.get("/{user_id}")
async def get_balance(user_id: str):
    collection = db.ledger
    balance = 0
    for document in collection.find({"userId": user_id}, {"amount": 1}): 
        balance += document["amount"]
    print (balance)
    return {"balance": balance}

@app.post("/", status_code=status.HTTP_201_CREATED, response_model=Ledger)
async def create_ledger(ledger: Ledger):
    collection = db.ledger
    ledger = jsonable_encoder(ledger)
    new_ledger = collection.insert_one(ledger)
    created_ledger = collection.find_one({"_id": new_ledger.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_ledger)