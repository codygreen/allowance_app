import motor
from beanie import init_beanie
from fastapi import FastAPI
from pydantic import BaseSettings

from models import Family
from routes import family_router

app = FastAPI()


class Settings(BaseSettings):
    mongodb_url = "mongodb://localhost:27017/allowance"


@app.on_event("startup")
async def app_init():
    client = motor.motor_asyncio.AsyncIOMotorClient(Settings().mongodb_url)
    await init_beanie(client.get_default_database(), document_models=[Family])
    app.include_router(family_router, prefix="/v1/family")