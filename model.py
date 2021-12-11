from pydantic import BaseModel

class Post(BaseModel):
    title: str
    description: str

class User(BaseModel):
    id: str
    name: str
    email: str
    pw: str
    orgs: list
    polls: list

