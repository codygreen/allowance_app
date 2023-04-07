"""Family Data Models"""
from beanie import Document, PydanticObjectId
class Family(Document):
    """Family Document"""
    name: str
    guardians: list[PydanticObjectId]

    class Config:
        """Family Schema Example"""
        schema_extra = {
            "example": {
                "name": "Green",
                "guardians": [
                    "642b03b9f0d9fe0007309f0e",
                    "642b050c62d9566c1c02abe5"
                ]
            }
        }
