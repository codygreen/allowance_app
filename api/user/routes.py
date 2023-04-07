from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from beanie import PydanticObjectId

from models import User

users_router = APIRouter()

async def get_user(user_id: PydanticObjectId) -> User:
    user = await User.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    return user

@users_router.get("/", response_model=List[User])
async def get_users():
    return await User.find_all().to_list()

@users_router.get("/{user_id}", response_model=User)
async def get_user_by_id(user: User = Depends(get_user)):
    return user

@users_router.post("/", status_code=status.HTTP_201_CREATED,
                   response_model=User)
async def create_user(user: User):
    return await user.insert()

@users_router.put("/{user_id}", response_model=User)
async def update_user(update_user: User, user: User = Depends(get_user)):
    # since the put body does not include the id, we need to set it
    update_user.id = user.id
    # update the user
    await update_user.save()
    return update_user

@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: User = Depends(get_user)):
    await user.delete()
