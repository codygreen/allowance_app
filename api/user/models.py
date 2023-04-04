from beanie import Document
from pydantic import BaseModel, Field
from beanie import PydanticObjectId

class User(Document):
    name: str
    password: str
    type: str
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
