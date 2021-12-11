from sqlalchemy.orm import Session
from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session):
    return db.query(models.User).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def deserialize_poll(db_poll: models.Poll) -> schemas.Poll:
    results_list = list(db_poll.results)
    choices_list = list(db_poll.choices)
    results = [schemas.Result(**res) for res in results_list]
    choices = [schemas.Choice(**choice) for choice in choices_list]
    
    poll = schemas.Poll(**db_poll, results=results, choices=choices)
    return poll

def serialize_poll(poll: schemas.PollCreate) -> models.Poll:
    db_poll = models.Poll(**poll, results=str(poll.results), choices=str(poll.choices))
    print(**db_poll)
    return db_poll


def get_poll(db: Session, poll_id: int) -> schemas.Poll:
    db_poll = db.query(models.Poll).filter(models.Poll.id == poll_id).first()
    return deserialize_poll(db_poll)

def get_polls(db: Session):
    return [deserialize_poll(poll) for poll in  db.query(models.Poll).all()]

def create_poll(db: Session, poll schemas.PollCreate):
    db_poll = serialize_poll(poll)
    db.add(db_poll)
    db.commit()
    db.refresh(db_poll)
    return db_poll


