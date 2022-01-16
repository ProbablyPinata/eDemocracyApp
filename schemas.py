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
    pw: str
    organisations: List[str]

class UserCreate(UserBase):
    pass

class User(UserBase):
    key: str


class Result(BaseModel):
    choice: int
    votes: int

class Choice(BaseModel):
    description: str
    id: int

class PollBase(BaseModel):
    name: str
    description: str
    anonymous: bool
    total_votes: int
    start_time: DateTime
    end_time: DateTime
    organisation_key: str
    results: List[Result]
    choices: List[Choice]

class PollCreate(PollBase):
    pass

class Poll(PollBase):
    key:str 



class OrganisationBase(BaseModel):
    name: str
    description: str
    admins: List[str]

class OrganisationCreate(OrganisationBase):
    pass

class Organisation(OrganisationBase):
    key:str
