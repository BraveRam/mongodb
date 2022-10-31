from pyrogram import Client, filters
from pyrogram.types import *

admin = 1365625365

api_id = 12501338
api_hash = "d2f2d3b3eae3df3dac595d3c8f55d443"
bot_token = "5769907387:AAFqJtPhZa1aj6wKH4qLei7-g4npfNVswTA"
app = Client(
  "Python",
  api_id=api_id,
  api_hash=api_hash,
  bot_token=bot_token
)

from motor.motor_asyncio import AsyncIOMotorClient as MongoClient # You can use pymongo module also
MONGO = "mongodb+srv://Really651:<751115_Lencho>@clusterbot.t2jjdwe.mongodb.net/?retryWrites=true&w=majority" # mongo db url here
mongo = MongoClient(MONGO)
mongodb = mongo.bot # You can change mongo.bot -> mongo.anything to use many bots/apps on same MONGO_URL
##################### USERS DB #####################
usersdb = mongodb.users

async def is_user(user_id: int) -> bool:
    user = await usersdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True

async def get_users() -> list:
    users_list = []
    async for user in usersdb.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list
    
async def add_user(user_id: int):
    is_served = await is_user(user_id)
    if is_served:
        return
    return await usersdb.insert_one({"user_id": user_id})    

@app.on_message(filters.command("start"))
async def strat(cilent, message):
      user_id = message.from_user.id
      if not await is_user(user_id):
         await add_user(user_id)
         a = message.from_user.mention
         b = message.from_user.id
         c = len(await get_users())
         app.send_message(b, f"Stats {c} Name {a}")

app.run()
