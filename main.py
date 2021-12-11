from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = ['https://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {'Ping: Pong'}


@app.get("/api/post")
async def get_post():
    return 1

@app.get("/api/post{id}")
async def get_post_by_id(id):
    return 1

@app.post("/api/post")
async def create_post(post):
    return 1

@app.put("/api/post{id}")
async def update_post(id, data):
    return 1

@app.delete("/api/post{id}")
async def delete_post(id):
    return 1