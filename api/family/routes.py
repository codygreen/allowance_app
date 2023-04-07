"""Family API routes"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from beanie import PydanticObjectId

from models import Family

family_router = APIRouter()

async def get_family(family_id: PydanticObjectId) -> Family:
    """Get a family by id"""
    family = await Family.get(family_id)
    if not family:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Family with id {family_id} not found",
        )
    return family

@family_router.get("/", response_model=List[Family])
async def get_families():
    """Get all families"""
    return await Family.find_all().to_list()

@family_router.get("/{family_id}", response_model=Family)
async def get_family_by_id(family: Family = Depends(get_family)):
    """Get a family by id"""
    return family

@family_router.post("/", status_code=status.HTTP_201_CREATED,
                    response_model=Family)
async def create_family(family: Family):
    """Create a new family"""
    return await family.insert()

@family_router.put("/{family_id}", response_model=Family)
async def update_family(u_family: Family, family: Family = Depends(get_family)):
    """Update a family"""
    # since the put body does not include the id, we need to set it
    u_family.id = family.id
    # update the family
    await u_family.save()
    return u_family

@family_router.delete("/{family_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_family(family: Family = Depends(get_family)):
    """Delete a family"""
    await family.delete()
