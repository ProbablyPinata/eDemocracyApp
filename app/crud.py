from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
import models, schemas

def serialize_user(user: schemas.UserCreate):
    db_user = models.User(**user.dict(exclude={'organisations'}), organisations=str(user.organisations))
    print(db_user)
    return db_user

def deserialize_user(db_user: models.User):
    if not db_user: return None
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

def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True

def deserialize_poll(db_poll: models.Poll) -> schemas.Poll:
    # TODO: check this
    
    if not db_poll: return None
    print("45", db_poll.results)
    results_list = db_poll.results.split(";")[0:-1]
    print("47", results_list[0])
    results = []
    for item in results_list:
        t = item.split("@")
        results.append(schemas.Result(choice=int(t[0]), votes=int(t[1])))
    choices_list = db_poll.choices.split(";")[0:-1]
    choices = []
    for item in choices_list:
        t = item.split("@")
        choices.append(schemas.Choice(id=int(t[0]), description=t[1]))
    print(results, choices)
    db_poll.results = results
    db_poll.choices = choices
    return db_poll

def serialize_poll(poll: schemas.PollCreate) -> models.Poll:
    print(poll.results)
    res_str = ""
    for res in poll.results:
        res_str += str(res.choice) + "@" + str(res.votes) + ";"
    print(res_str)

    cho_str = ""
    for choice in poll.choices:
        cho_str += str(choice.id) + "@" + str(choice.description) + ";"
    print(cho_str)
    db_poll = models.Poll(**poll.dict(exclude={'results', 'choices'}), results=res_str, choices=cho_str)
    print("74", db_poll.results)
    return db_poll


def get_poll(db: Session, poll_id: int) -> schemas.Poll:
    db_poll = db.query(models.Poll).filter(models.Poll.id == poll_id).first()
    print("80", db_poll.results)
    return deserialize_poll(db_poll)

def get_polls(db: Session):
    return [deserialize_poll(poll) for poll in  db.query(models.Poll).all()]

def create_poll(db: Session, poll: schemas.PollCreate):
    db_poll = serialize_poll(poll)
    db.add(db_poll)
    db.commit()
    db.refresh(db_poll)
    return deserialize_poll(db_poll)

def delete_poll(db: Session, poll_id: int):
    poll = get_poll(db, poll_id)
    if not poll:
        return False
    db.delete(poll)
    db.commit()
    return True

def add_poll_vote(db: Session, poll_id: int, choice: int):
    poll = get_poll(db, poll_id)
    if not poll:
        return None
    for result in poll.results:
        if result.choice == choice:
            result.votes += 1
            break
    print(poll.results)
    res_str = ""
    for res in poll.results:
        res_str += str(res.choice) + "@" + str(res.votes) + ";"
    print(res_str)

    poll.results = res_str
    
    cho_str = ""
    for choice in poll.choices:
        cho_str += str(choice.id) + "@" + str(choice.description) + ";"
    print(cho_str)
    poll.choices = cho_str
    print("111", poll.results)
    db.query(models.Poll).filter(models.Poll.id == poll_id).update({models.Poll.results: poll.results}, synchronize_session=False)
    db.commit()
    return get_poll(db, poll_id)

def serialize_organisation(org: schemas.OrganisationCreate) -> models.Organisation:
    db_org = models.Organisation(**org.dict(exclude={'admins'}), admins=str(org.admins))
    print(db_org)
    return db_org

def deserialize_organisation(db_org: models.Organisation) -> schemas.Organisation:
    if not db_org: return None
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

def delete_organisation(db: Session, org_id: int):
    org = get_organisation(db, org_id)
    if not org:
        return False
    db.delete(org)
    db.commit()
    return True
