"""User Redis Worker"""
import asyncio
import random
import string
import sys
from os import environ
# from utils import Consumer
import motor
from beanie import PydanticObjectId, init_beanie
from models import User
from redis import Redis
from routes import get_user

# pylint: disable=wrong-import-position
sys.path.append('../utils')
from utils import Consumer

redis_hostname = environ.get('REDIS_HOSTNAME', 'localhost')
redis_port = environ.get('REDIS_PORT', 6379)
stream_name = environ.get('REDIS_STREAM_NAME', 'user')
group_name = environ.get('REDIS_GROUP_NAME', 'user_group')
worker_name = environ.get('REDIS_WORKER_NAME',
                          ''.join(random.choices(string.ascii_lowercase +
                             string.digits, k=7)))

mongo_hostname = environ.get('MONGO_HOSTNAME', 'localhost')
mongo_port = environ.get('MONGO_PORT', 27017)
mongo_db = environ.get('MONGO_DB', 'allowance')
mongo_url = f"mongodb://{mongo_hostname}:{mongo_port}/{mongo_db}"

async def init():
    """Main Worker"""
    # connect to redis
    redis = Redis(redis_hostname, redis_port, db=0, decode_responses=True)
    # connect to mongo
    client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
    # init beanie
    await init_beanie(client.get_default_database(), document_models=[User])

    consumer = Consumer(redis, stream_name, group_name, worker_name)
    while True:
        events = consumer.get_events()
        for i, event in enumerate(events):
            print(f"EVENT: {event}")
            await process_event(event)
            consumer.ack_event(i)

async def process_event(event):
    """Process Redis Event"""
    print(f"PROCESSING EVENT: {event}")
    message = event[1]
    data = message[0][1]
    if data:
        user_id = data.get('user_id')
        amount = data.get('amount')
        data_type = data.get('type')
        if user_id and amount and data_type == 'update_balance':
            await update_balance(user_id, amount)
    return

async def update_balance(user_id, amount):
    """Update User Balance"""
    user = await get_user(PydanticObjectId(user_id))
    if user:
        user.balance += float(amount)
        await user.save()
    else:
        print("ERROR: USER NOT FOUND")
    return

if __name__ == '__main__':
    asyncio.run(init())
