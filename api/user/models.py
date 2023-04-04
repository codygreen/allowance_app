from beanie import Document
from pydantic import BaseModel, Field
from beanie import PydanticObjectId
from typing import Literal 


class User(Document):
    name: str
    password: str
    type: Literal["guardian", "child", "contributor"]
    familyId: PydanticObjectId

    class Config:
        schema_extra = {
            "example": {
                "name": "John",
                "password": "1234",
                "type": "guardian",
                "familyId": "642b09500fec1b9fe4ab78ae"
            }
        }
