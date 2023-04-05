import motor
from beanie import init_beanie, PydanticObjectId
from pydantic import BaseSettings
from redis import Redis
from os import environ
import asyncio

from models import User
from routes import get_user

redis_hostname = environ.get('REDIS_HOSTNAME', 'localhost')
redis_port = environ.get('REDIS_PORT', 6379)
stream_name = environ.get('REDIS_STREAM_NAME', 'user')

mongo_hostname = environ.get('MONGO_HOSTNAME', 'localhost')
mongo_port = environ.get('MONGO_PORT', 27017)
mongo_db = environ.get('MONGO_DB', 'allowance')
mongo_url = "mongodb://{}:{}/{}".format(mongo_hostname, mongo_port, mongo_db)

async def init():
    redis = Redis(redis_hostname, redis_port, db=0, decode_responses=True)
    client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
    await init_beanie(client.get_default_database(), document_models=[User])
    await get_redis_data(redis, stream_name)

async def get_redis_data(redis, stream_name):
    while True:
        try:
            event = redis.xread({stream_name: '$'}, count=1, block=0)
            if event:
                key, message = event[0]
                last_id, data = message[0]
                print("REDIS ID: {}".format(last_id))
                print("      --> {}".format(data))
                
                if(data.get('type') == 'update_balance'):
                    await update_balance(data.get('user_id'), data.get('amount'))
                    
        except ConnectionError as e:
            print("ERROR REDIS CONNECTION: {}".format(e))

async def update_balance(user_id, amount):
    user = await get_user(PydanticObjectId(user_id))
    if user:
        user.balance += float(amount)
        await user.save()
    else:
        print("ERROR: USER NOT FOUND")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init())
    loop.run_forever()
    loop.close()