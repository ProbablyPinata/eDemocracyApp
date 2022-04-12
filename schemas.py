from typing import List, Optional
from pydantic import BaseModel


class DateTime(BaseModel):
    year: int
    month: int
    day: int
    hours: int
    minutes: int

class UserBase(BaseModel):
    name: str
    email: str
    password: str
    organisations: List[str]

class UserCreate(UserBase):
    pass

class User(UserBase):
    key: str


class Result(BaseModel):
    choice: int
    votes: int
    who_voted: List[str] # who voted (key) #SAM - changed this from a string to a list

class Choice(BaseModel):
    description: str
    id: int

class PollBase(BaseModel):
    name: str
    description: str
    anonymous: bool
    start_time: DateTime # epoch time
    end_time: DateTime # epoch time
    organisation_key: str

class PollCreate(PollBase):
    choices: List[str]
    pass

class Poll(PollBase):
    choices: List[Choice] =[]
    results: List[Result] = []
    total_votes: int = 0
    key:str = ""
    organisation_name: str = ""

class PollView(PollBase):
    choices: List[Choice] =[]
    organisation_name: str = ""

class OrganisationBase(BaseModel):
    name: str
    description: str
    admins: List[str]

class OrganisationCreate(OrganisationBase):
    pass

class Organisation(OrganisationBase):
    key:str
