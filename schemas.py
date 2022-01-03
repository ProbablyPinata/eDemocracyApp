from typing import List, Optional
from pydantic import BaseModel
import datetime

class UserBase(BaseModel):
    name: str
    email: str
    pw: str
    organisations: List[int]

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
    start_time: datetime.datetime
    end_time: datetime.datetime
    organisation_id: int
    results: List[Result]
    choices: List[Choice]

class PollCreate(PollBase):
    pass

class Poll(PollBase):
    key:str 



class OrganisationBase(BaseModel):
    name: str
    description: str
    admins: List[int]

class OrganisationCreate(OrganisationBase):
    pass

class Organisation(OrganisationBase):
    key:str

