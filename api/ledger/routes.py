from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from beanie import PydanticObjectId

from models import Ledger

ledger_router = APIRouter()

async def get_ledger(ledger_id: PydanticObjectId) -> Ledger:
    ledger = await Ledger.get(ledger_id)
    if not ledger:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ledger with id {ledger_id} not found",
        )
    return ledger

# CRUD
@ledger_router.get("/{ledger_id}", response_model=Ledger)
async def get_ledger_by_id(ledger: Ledger = Depends(get_ledger)):
    return ledger

@ledger_router.post("/", status_code=status.HTTP_201_CREATED,
                    response_model=Ledger)
async def create_ledger(ledger: Ledger):
    return await ledger.insert()

@ledger_router.put("/{ledger_id}", response_model=Ledger)
async def update_ledger(update_ledger: Ledger, ledger: Ledger = Depends(get_ledger)):
    # since the put body does not include the id, we need to set it
    update_ledger.id = ledger.id
    # update the ledger
    await update_ledger.save()
    return update_ledger

@ledger_router.delete("/{ledger_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ledger(ledger: Ledger = Depends(get_ledger)):
    await ledger.delete()

# Lists
@ledger_router.get("/", response_model=List[Ledger])
async def get_ledgers(limit: int = 10):
    return await Ledger.find_all().limit(limit).to_list()

# Find by user id
@ledger_router.get("/user/{user_id}", response_model=List[Ledger])
async def get_ledgers_by_user_id(user_id: str, state: str = None, limit: int = 10):
    if state:
        return await Ledger.find(Ledger.userId == user_id, Ledger.state == state).limit(limit).to_list()
    return await Ledger.find(Ledger.userId == user_id).limit(limit).to_list()


