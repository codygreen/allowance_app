"""User API Routes"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from beanie import PydanticObjectId

from models import User

users_router = APIRouter()

async def get_user(user_id: PydanticObjectId) -> User:
    """Get a user from database by id"""
    user = await User.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    return user

@users_router.get("/", response_model=List[User])
async def get_users():
    """Get all users from database"""
    return await User.find_all().to_list()

@users_router.get("/{user_id}", response_model=User)
async def get_user_by_id(user: User = Depends(get_user)):
    """Get a user from database by id"""
    return user

@users_router.post("/", status_code=status.HTTP_201_CREATED,
                   response_model=User)
async def create_user(user: User):
    """Create a new user in the database"""
    return await user.insert()

@users_router.put("/{user_id}", response_model=User)
async def update_user(u_user: User, user: User = Depends(get_user)):
    """Update the user data in the database"""
    # since the put body does not include the id, we need to set it
    u_user.id = user.id
    # update the user
    await u_user.save()
    return u_user

@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: User = Depends(get_user)):
    """Delete the user from the database"""
    await user.delete()
