from beanie import Document
from pydantic import BaseModel, Field
from beanie import PydanticObjectId
from typing import Literal 
from datetime import datetime

class Ledger(Document):
    userId: PydanticObjectId
    amount: int
    type: Literal["allowance", "chores", "deposit", "withdrawal", "gift"]
    state: Literal["pending", "successful"] = Field(default="pending")
    date: datetime = Field(default=datetime.now())

    class Config:
        schema_extra = {
            "example": {
                "userId": "642b09500fec1b9fe4ab78ae",
                "amount": 100,
                "type": "gift",
                "state": "successful",
                "date": "2032-04-23T10:20:30.400+02:30"
            }
        }
