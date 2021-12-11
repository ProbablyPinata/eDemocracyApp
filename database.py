from typing import Collection
from model import Post
import motor.motor_asyncio  # mongo db driver

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
db = client.PostList
collection = db.post


# MAIN FUNCTIONALITY
async def fetch_post(title):
    document = await collection.find_one({'title':title})
    return document

async def fetch_all():
    posts = []
    cursor = collection.find({})
    async for document in cursor:
        posts.append(Post(**document))
    return posts


async def create_post(post):
    document = post
    result = await collection.insert_one(document)
    return document

async def update_post(title, description):
   await collection.update_one() 