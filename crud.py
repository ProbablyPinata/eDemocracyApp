from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
import models, schemas

def serialize_user(user: schemas.UserCreate):
    db_user = models.User(**user.dict(exclude={'organisations'}), organisations=str(user.organisations))
    print(db_user)
    return db_user

def deserialize_user(db_user: models.User):
    orgs_list = list(db_user.organisations)[1:-1]
    print(orgs_list)
    orgs = [int(org) for org in orgs_list]
    print("organisations", orgs)
    db_user.organisations = orgs
    return db_user


def get_user(db: Session, user_id: int):
    return deserialize_user(db.query(models.User).filter(models.User.id == user_id).first())

def get_users(db: Session):
    return [deserialize_user(user) for user in db.query(models.User).all()]

def create_user(db: Session, user: schemas.UserCreate):
    db_user = serialize_user(user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return deserialize_user(db_user)

def deserialize_poll(db_poll: models.Poll) -> schemas.Poll:
    # TODO: check this
    results_list = list(db_poll.results)[1:-1]
    choices_list = list(db_poll.choices)[1:-1]
    results = [schemas.Result(**res) for res in results_list]
    choices = [schemas.Choice(**choice) for choice in choices_list]
    
    db_poll.results = results
    db_poll.choices = choices
    return db_poll

def serialize_poll(poll: schemas.PollCreate) -> models.Poll:
    db_poll = models.Poll(**poll.dict(exclude={'results', 'choices'}), results=str(poll.results), choices=str(poll.choices))
    print(db_poll)
    return db_poll


def get_poll(db: Session, poll_id: int) -> schemas.Poll:
    db_poll = db.query(models.Poll).filter(models.Poll.id == poll_id).first()
    return deserialize_poll(db_poll)

def get_polls(db: Session):
    return [deserialize_poll(poll) for poll in  db.query(models.Poll).all()]

def create_poll(db: Session, poll: schemas.PollCreate):
    db_poll = serialize_poll(poll)
    db.add(db_poll)
    db.commit()
    db.refresh(db_poll)
    return deserialize_poll(db_poll)

def serialize_organisation(org: schemas.OrganisationCreate) -> models.Organisation:
    db_org = models.Organisation(**org.dict(exclude={'admins'}), admins=str(org.admins))
    print(db_org)
    return db_org

def deserialize_organisation(db_org: models.Organisation) -> schemas.Organisation:
    admin_list = list(db_org.admins)[1:-1]
    admins = [int(admin) for admin in admin_list]
    db_org.admins = admins
    return db_org

def get_organisation(db: Session, org_id: int):
    db_org = db.query(models.Organisation).filter(models.Organisation.id == org_id).first()
    return deserialize_organisation(db_org)

def get_organisations(db: Session):
    return [deserialize_organisation(org) for org in db.query(models.Organisation).all()]

def create_organisation(db: Session, org: schemas.OrganisationCreate):
    db_org = serialize_organisation(org)
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return deserialize_organisation(db_org)