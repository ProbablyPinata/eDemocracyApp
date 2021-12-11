from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import *

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
    


# User management
@app.post("/users/add")
async def add_user(name, email, pw, orgs, polls):
    return True

@app.delete("/users/delete/{id}/")
async def delete_user(id):
    return True


@app.put("/users/email/{new_email}/")
async def update_user_email(id, new_email):
    return True

@app.put("/users/name/{new_name}/")
async def update_user_name(id, new_name):
    return True
"""

UPDATE /users/name/{new_name}/ = same as above 

UPDATE /users/password/{new_password}/ = same as above 

GET /users/{id} = gets the user 

 

POST /polls/add = adds a poll 

DELETE /polls/delete/{id}/{user_id} = only an admin can delete a poll. Deletes polls from others' history 

UPDATE /polls/name/{new_name}/ = and for description and any other fields that seem fitting 

POST /polls/add_vote/{user_id}/{choice_id}/ = votes for a person. Ensures person is in the organisation of the poll 

UPDATE /polls/change_vote/{user_id}/{new_choice} = changes a users' vote 

GET /polls/{id} = gets the poll 

 

POST /org/add/{creator_id} = we need a user to create an orgnaisation, and so that user will automatically be made an admin 

DELETE /org/delete/{id} = deletes organisation and related polls 

POST /org/add_admin/{id} = adds an admin 

DELETE /org/del_admin/{id} = removes an admin. If one admin remains this fails 

UPDATE /org/name/{new_name} = changes name 

UPDATE /org/description/{new_desc} 

DELETE /org/delete/{id}/{user_id} = only admin can delete organisation. Deletes the orgnaisation 

POST /org/invite/{email} = invites user with email. Adds the user but we may do an email invitation """