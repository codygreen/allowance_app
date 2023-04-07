"""User API Data Models"""
from typing import Literal
from beanie import Document, PydanticObjectId
from pydantic import Field


class User(Document):
    """User Document"""
    name: str
    type: Literal["guardian", "child", "contributor"]
    familyId: PydanticObjectId
    balance: float = Field(default=0)

    class Config:
        """Document Schema Example"""
        schema_extra = {
            "example": {
                "name": "John",
                "type": "guardian",
                "familyId": "642b09500fec1b9fe4ab78ae",
                "balance": 0
            }
        }
