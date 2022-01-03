from typing import List
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from deta import Deta
from schemas import *
app = FastAPI()
deta = Deta("a0svha7u_zdyC9BJGJLCzv36DdG5Y2RtHPMKiwK2Y")

users = deta.Base("users")
polls = deta.Base("polls")
organisations = deta.Base("organisations")


origins = ['https://localhost:3000']



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def validate(response):
    if response:
        return response
    raise HTTPException(400, 'something went wrong.')

@app.get("/")
def read_root():
    return {'Ping': 'Pong'}
"""

@app.get("/api/post")
async def get_post():
    response = await fetch_all()
    return response

@app.get("/api/post{title}", response_model=Post)
async def get_post_by_id(title):
    response = await fetch_post(title)
    if response:
        return response
    raise HTTPException(404, f'there is no POST item with this (id)')


@app.post("/api/post", response_model=Post)
async def new_post(post: Post):
    response = await create_post(post.dict())
    if response:
        return response
    raise HTTPException(400, 'bad request')

    

@app.put("/api/post{title}", response_model=Post)
async def put_post(title:str, description:str):
    response = await update_post(title, description)
    if response:
        return response
    raise HTTPException(404, f'there is no Post item with this (id)')

@app.delete("/api/post{title}")
async def delete_post(title):
    response = await delete_post(title)
    if response:
        return 'success'
    raise HTTPException(404, f'there is no Post item with this (id) to delete')

"""
# User management
@app.get("/users/name/{user_id}", response_model=User)
async def get_user_by_id(user_id):
    response = get_user(db, user_id)
    print(response)
    return validate(response)

@app.get("/users/", response_model=List[User])
async def get_all_users():
    response = get_users(db)
    return validate(response)

@app.post("/users/add", response_model=User)
async def new_user(user: UserCreate):
    response = create_user(db, user)
    return validate(response)

@app.delete("/users/delete/{user_id}")
def app_delete_user(user_id: int):
    if not delete_user(user_id, db):
        raise HTTPException(400, "Unable to delete user")

# Poll management
"""
@app.post("/polls/add", response_model=Poll)
async def new_poll(poll: schemas.PollCreate):
    response = create_poll(db, poll)
    return validate(response)

@app.post("/poll/{poll_id}", response_model=Poll)
async def get_poll_by_id(poll_id: int):
    response = get_poll(db, poll_id)
    return validate(response)

@app.post("/polls/get/all", response_model=List[Poll])
async def get_all_polls():
    response = get_polls(db)
    return validate(response)

@app.post("/polls/", response_model=List[Poll])
async def yourmum():
    response = get_polls(db)
    return validate(response)

@app.post("/polls/add_vote/{poll_id}/{choice_id}", response_model=Poll)
def add_vote(poll_id: int, choice_id: int):
    # check if user is in organisation. For later

    response = add_poll_vote(db, poll_id, choice_id)
    return validate(response)

@app.post("/org/add/{user_id}", response_model=Organisation)
def add_org(user_id: int):
    pass

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(user_id: int, item: schemas.ItemCreate):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@app.delete("/users/delete/{id}/")
async def delete_user(id):
    return True


@app.put("/users/email/{new_email}/")
async def update_user_email(id, new_email):
    return True

@app.put("/users/name/{new_name}/")
async def update_user_name(id, new_name):
    return True

@app.put("/users/name/{new_password}/")
async def update_user_password(id, new_password):
    return True
"""
