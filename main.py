from re import L
from typing import List
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from deta import Deta
from schemas import *

VER_MAJOR = 0
VER_MINOR = 1
VER_PATCH = "branch-basic-auth.1"

app = FastAPI()
deta = Deta("a0svha7u_zdyC9BJGJLCzv36DdG5Y2RtHPMKiwK2Y")
security = HTTPBasic()

users = deta.Base("users")
polls = deta.Base("polls")
organisations = deta.Base("organisations")


origins = ['http://localhost:8000', 'http://localhost:3000']




app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def creds_error():
    raise HTTPException(
            status_code=401,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Basic"}
        )

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    user = users.fetch({"email": credentials.username})

    if len(user.items) == 0:
        creds_error()
    user = user.items[0]
    username_correct = secrets.compare_digest(credentials.username, user["email"])
    password_correct = secrets.compare_digest(credentials.password, user["password"])
    if not (username_correct and password_correct):
        creds_error()
    return user

def validate(response):
    if response:
        return response
    raise HTTPException(400, 'something went wrong.')

@app.get("/")
def read_root():
    return {'Ping': 'Pong'}

@app.get("/admin/version")
def version():
    return {"Major": VER_MAJOR,
            "Minor": VER_MINOR,
            "Patch": VER_PATCH}

def delete_all_fields(db):
    res = db.fetch()
    all_items = res.items
    while res.last:
        res = db.fetch(last=res.last)
        all_items += res.items
    
    for item in all_items:
        db.delete(item["key"])

@app.get("/admin/delete_all")
def delete_all(user: User = Depends(authenticate)):
    if user.email != "admin":
        creds_error()
    delete_all_fields(users)
    delete_all_fields(polls)
    delete_all_fields(organisations)

# User management
@app.get("/users/{key}", response_model=User)
def get_user_by_key(key: str, user: User = Depends(authenticate)):
    return validate(user)

@app.get("/users/", response_model=List[User])
def get_all_users(user: User = Depends(authenticate)):
    response = users.fetch()
    return validate(response.items)

@app.post("/users/add", response_model=User )
def new_user(user: UserCreate):
    user = users.put(user.dict())
    print(user)
    return user

@app.delete("/users/delete/{key}")
def delete_user(key: str, user: User = Depends(authenticate)):
    if user.key != key:
        creds_error()
    print(users.get(key))
    user_organisations = organisations.fetch({"admins?contains": key})
    print("user is in", user_organisations.items)
    while user_organisations.last:
        for organisation in user_organisations.items:
            organisation["admins"].remove(key)
            organisations.update(organisation, organisation["key"])
        user_organisations = organisations.fetch(lest=user_organisations.last)
    users.delete(key)

# Poll management
# validate emails, store user votes 
@app.post("/polls/add", response_model=Poll)
def new_poll(poll: PollCreate, user: User = Depends(authenticate)):
    org = poll.organisation_key
    if organisations.get(org) is None:
        raise HTTPException(404, "Unable to add poll")
    
    new_poll = Poll(**poll)
    nextID = 1 #
    
    # fill in choices and results array for new_poll using poll.choices
    if poll.results == []: # Results are not filled
        for choice in poll.choices:
            # poll.results.append(Result(choice=choice.id, votes=0))
            new_poll.results.append(Result(choice=nextID, votes=0)) #
            nextID += 1 #
    poll = polls.put(new_poll.dict())
    print("Ok")
    return validate(new_poll)

@app.get("/poll/{key}", response_model=Poll)
def get_poll_by_id(key: str, user: User = Depends(authenticate)):

    poll = polls.get(key)
    if poll.organisation_key not in user.organisations:
        creds_error()
    return validate(poll)

@app.get("/polls/{organisation}", response_model=List[Poll])
def get_all_polls(organisation: str, user: User = Depends(authenticate)):

    response = polls.fetch()
    return validate(response.items)

@app.delete("/polls/delete/{key}")
def delete_poll(key: str, user: User = Depends(authenticate)):
    poll = get_poll_by_id(key, user)
    organisation = get_organisation_by_key(poll.organisation_key)
    if user.key not in organisation.admins:
        creds_error()
    polls.delete(key)

@app.post("/polls/add_vote/{key}/{choice_id}", response_model=Poll)
def add_vote(key: str, choice_id: int, user: User = Depends(authenticate)):
    # check if user is in organisation. For later when we do oauth
    
    poll = get_poll_by_id(key)
    if poll.organisation_key not in user.organisations:
        creds_error()
    found = False
    for choice in poll["choices"]:
        if choice["id"] == choice_id:
            found = True
            break
    if not found:
        raise HTTPException(404, "Unable to add choice") # be ambiguous to avoid hackers
    for result in poll["results"]:
        if result["choice"] == choice_id:
            result["votes"] += 1
            break
    updates = {"results": poll["results"]}
    print(poll)
    poll = polls.update(updates, key)
    
    return validate(polls.get(key))

# Organisation management
@app.get("/organisations/{key}", response_model=Organisation)
def get_organisation_by_key(key: str, user: User = Depends(authenticate)):
    # TODO: have organisations which you can/can't join
    org = organisations.get(key)
    return validate(org)

@app.get("/organisations/", response_model=List[Organisation])
def get_all_organisations(user: User = Depends(authenticate)):
    response = organisations.fetch()
    return validate(response.items)

@app.post("/organisations/add", response_model=Organisation)
def new_organisation(org: OrganisationCreate, user: User = Depends(authenticate)):
    org = organisations.put(org.dict())
    return org

@app.delete("/organisations/delete/{key}")
def app_delete_organisation(key: str, user: User = Depends(authenticate)):
    # Should go through and remove all organisations from users
    organisation = get_organisation_by_key(key)
    if user.key not in organisation.admins:
        creds_error()

    for user in get_all_users():
        if key in user["organisations"]:
            user["organisations"].remove(key)
    
    polls_to_delete = polls.fetch({"organisation_key": key})
    for poll in polls_to_delete.items:
        polls.delete(poll["key"])
    
    organisations.delete(key)

@app.post('/organisations/add_admin/{org_key}/{admin_key}')
def add_organisation_admin(org_key: str, admin_key: str, user: User = Depends(authenticate)):
    # TODO: send an email to existing admins
    organisations.update({"admins": organisations.util.append(admin_key)}, org_key)
    return organisations.get(org_key)
"""
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
