from __future__ import annotations
import main
from fastapi.testclient import TestClient
from schemas import *

client = TestClient(main.app)


def test_sanity():
    response = client.get('/')
    assert response.json() == {"Ping": "Pong"}


def test_users():
    user1 = UserCreate(name="test1",
                       email="test1",
                       pw="test_pw",
                       organisations=[])
    response = client.post('/users/add', data=user1.json())
    assert response.status_code == 200
    key = response.json()["key"]
    user1 = response.json()

    response = client.get(f'/users/{key}')
    assert response.json() == user1

    response = client.get('/users/')
    assert user1 in response.json()

    client.delete(f'/users/delete/{key}')
    assert response.status_code == 200


def test_organisations():
    user1 = UserCreate(name="test1",
                       email="test1",
                       pw="test_pw",
                       organisations=[])
    response = client.post('/users/add', data=user1.json())
    user1 = response.json()
    org1 = OrganisationCreate(name="test1",
                              description="",
                              admins=[user1["key"]])
    response = client.post("/organisations/add", data=org1.json())
    assert response.status_code == 200
    org1 = response.json()

    user2 = UserCreate(name="test2",
                       email="test2",
                       pw="test_pw",
                       organisations=[])
    response = client.post('/users/add', data=user2.json())
    user2 = response.json()

    response = client.post(
        f'/organisations/add_admin/{org1["key"]}/{user2["key"]}')
    assert user2["key"] in response.json()["admins"]
    org1 = response.json()

    response = client.get(f'/organisations/{org1["key"]}')
    assert response.json() == org1

    response = client.get("/organisations/")
    assert org1 in response.json()

    client.delete(f'/users/delete/{user1["key"]}')
    client.delete(f'/users/delete/{user2["key"]}')
    response = client.delete(f'/organisations/delete/{org1["key"]}')
    assert response.status_code == 200


def test_polls():

    user1 = UserCreate(name="test1",
                       email="test1",
                       pw="test_pw",
                       organisations=[])
    response = client.post('/users/add', data=user1.json())
    user1 = response.json()
    org1 = OrganisationCreate(name="test1",
                              description="",
                              admins=[user1["key"]])
    response = client.post("/organisations/add", data=org1.json())
    org1 = response.json()
    assert response.status_code == 200

    poll1 = PollCreate(name="test", description="poll", anonymous=False, \
        start_time=DateTime(year=0, month=0, day=0, hours=0, minutes=0), \
            end_time=DateTime(year=0, month=0, day=0, hours=0, minutes=0)\
                , organisation_key=org1["key"], \
                    choices=[Choice(description="choice1", id=1)], results=[])
    response = client.post("/polls/add", data=poll1.json())
    assert response.status_code == 200
    poll1 = response.json()

    response = client.get(f'/poll/{poll1["key"]}')
    assert response.json() == poll1

    response = client.get("/polls")
    assert poll1 in response.json()

    response = client.post(f'/polls/add_vote/{poll1["key"]}/{1}')
    assert response.json()['results'][0]["votes"] == 1

    client.delete(f'/polls/delete/{poll1["key"]}')