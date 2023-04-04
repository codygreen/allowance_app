from beanie import Document
from pydantic import BaseModel, Field
from beanie import PydanticObjectId

class Family(Document):
    name: str
    guardians: list[PydanticObjectId]

    class Config:
        schema_extra = {
            "example": {
                "name": "Green",
                "guardians": [
                    "642b03b9f0d9fe0007309f0e",
                    "642b050c62d9566c1c02abe5"
                ]
            }
        }
