from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import descriptor_props, relationship
from .database import Base
from pydantic import BaseModel

# can you see this? yes
# nice


class User(Base):
    __tablename__ = "users"

    #id: str
    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    email = Column(String, unique=True)
    pw = Column(String)
    organisations = Column(String)


class Poll(Base):
    __tablename__ = "polls"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    anonymous = Column(Boolean)
    total_votes = Column(Integer)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    organisation_id = Column(Integer, ForeignKey("organisation.id"))
    results = Column(String) # [{choice: id, votes: int}]
    choices = Column(String) # [{description: int, id: int}]


    organisation = relationship("Organisation", back_populates="poll")

class Organisation(Base):
    __tablename__ = "organisations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    admins = Column(String)
    poll = relationship("Poll", back_populates="organisation")
