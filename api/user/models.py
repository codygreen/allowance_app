from beanie import Document
from pydantic import BaseModel, Field
from beanie import PydanticObjectId
from typing import Literal 


class User(Document):
    name: str
    type: Literal["guardian", "child", "contributor"]
    familyId: PydanticObjectId
    balance: float = Field(default=0)

    class Config:
        schema_extra = {
            "example": {
                "name": "John",
                "type": "guardian",
                "familyId": "642b09500fec1b9fe4ab78ae",
                "balance": 0
            }
        }
