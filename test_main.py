import main
from fastapi.testclient import TestClient
from requests.auth import HTTPBasicAuth
from schemas import *

client = TestClient(main.app)


def test_sanity():
    response = client.get('/')
    assert response.json() == {"Ping": "Pong"}

username = "test"
password = "test_password"

username2 = "test2"
password2 = "pw2"

res = client.get("/admin/delete_all", auth=HTTPBasicAuth(username=main.ADMIN_EMAIL, password=main.ADMIN_PASSWORD))
assert res.status_code == 200

res = client.get("/admin/version")
assert res.json() == {"Major": main.VER_MAJOR, "Minor": main.VER_MINOR, "Patch": main.VER_PATCH} 


def test_users():
    user1 = UserCreate(name="test1",
                       email=username,
                       password=password,
                       organisations=[])
    response = client.post('/users/add', data=user1.json(), auth=HTTPBasicAuth(username=username, password=password))
    assert response.status_code == 200
    key = response.json()["key"]
    user1 = response.json()

    response = client.get(f'/users/{key}',auth=HTTPBasicAuth(username=username, password=password))
    assert response.json() == user1

    response = client.get('/users/',auth=HTTPBasicAuth(username=username, password=password))
    assert user1 in response.json()

    client.delete(f'/users/delete/{key}',auth=HTTPBasicAuth(username=username, password=password))
    assert response.status_code == 200


def test_organisations():
    user1 = UserCreate(name="test1",
                       email=username,
                       password=password,
                       organisations=[])
    response = client.post('/users/add', data=user1.json(), auth=HTTPBasicAuth(username=username, password=password))
    user1 = response.json()
    org1 = OrganisationCreate(name="test1",
                              description="",
                              admins=[user1["key"]])
    response = client.post("/organisations/add", data=org1.json(), auth=HTTPBasicAuth(username=username, password=password))
    assert response.status_code == 200
    org1 = response.json()

    user2 = UserCreate(name="test2",
                       email="test2",
                       password="test_password",
                       organisations=[])
    response = client.post('/users/add', data=user2.json(), auth=HTTPBasicAuth(username=username, password=password))
    user2 = response.json()

    response = client.post(
        f'/organisations/add_admin/{org1["key"]}/{user2["key"]}', auth=HTTPBasicAuth(username=username, password=password))
    assert user2["key"] in response.json()["admins"]
    org1 = response.json()

    response = client.get(f'/organisations/{org1["key"]}', auth=HTTPBasicAuth(username=username, password=password))
    assert response.json() == org1

    response = client.get("/organisations/", auth=HTTPBasicAuth(username=username, password=password))
    assert org1 in response.json()

    client.delete(f'/users/delete/{user2["key"]}', auth=HTTPBasicAuth(username=username, password=password))
    assert response.status_code == 200

    
    response = client.get(f'/organisations/{org1["key"]}', auth=HTTPBasicAuth(username=username, password=password))
    assert user2["key"] not in response.json()["admins"]

    response = client.delete(f'/organisations/delete/{org1["key"]}', auth=HTTPBasicAuth(username=username, password=password))
    
    client.delete(f'/users/delete/{user1["key"]}', auth=HTTPBasicAuth(username=username, password=password))
    
    assert response.status_code == 200


def test_polls():

    user1 = UserCreate(name="test1",
                       email=username,
                       password=password,
                       organisations=[])
    response = client.post('/users/add', data=user1.json(), auth=HTTPBasicAuth(username=username, password=password))
    user1 = response.json()
    org1 = OrganisationCreate(name="test1",
                              description="",
                              admins=[user1["key"]])
    response = client.post("/organisations/add", data=org1.json(), auth=HTTPBasicAuth(username=username, password=password))
    org1 = response.json()
    assert response.status_code == 200

    response = client.post(f'/users/add_organisation/{user1["key"]}/{org1["key"]}', auth=HTTPBasicAuth(username=username, password=password))
    assert response.status_code == 200
    user1 = response.json()
    poll1 = PollCreate(name="test", description="poll", anonymous=False, \
        start_time=DateTime(year=0, month=0, day=0, hours=0, minutes=0), \
            end_time=DateTime(year=0, month=0, day=0, hours=0, minutes=0)\
                , organisation_key=org1["key"], \
                    choices=["choice1"])
    response = client.post("/polls/add", data=poll1.json(), auth=HTTPBasicAuth(username=username, password=password))
    assert response.status_code == 200

    poll1 = response.json()
    
    response = client.get(f'/poll/{poll1["key"]}', auth=HTTPBasicAuth(username=username, password=password))
    assert response.json() == poll1

    
    response = client.post(f'/polls/add_vote/{poll1["key"]}/{1}', auth=HTTPBasicAuth(username=username, password=password))
    print(response.json())
    assert response.json()['results'][0]["votes"] == 1
    assert response.json()['results'][0]["who_voted"] == user1["key"]

    response = client.delete(f'/polls/delete/{poll1["key"]}', auth=HTTPBasicAuth(username=username, password=password))
    assert response.status_code == 200

def test_auth():
    res = client.get("/admin/delete_all", auth=HTTPBasicAuth(username=main.ADMIN_EMAIL, password=main.ADMIN_PASSWORD))
    assert res.status_code == 200

    user1 = UserCreate(name="test1",
                       email=username,
                       password=password,
                       organisations=[])
    
    response = client.post('/users/add', data=user1.json(), auth=HTTPBasicAuth(username=username, password=password))
    assert response.status_code == 200
    key = response.json()["key"]
    response = client.get(f'/users/{key}',auth=HTTPBasicAuth(username=username, password=password))
    assert response.status_code == 200
    response = client.get(f'/users/{key}',auth=HTTPBasicAuth(username="jksdjk", password=password))
    assert response.status_code == 401
    response = client.get(f'/users/{key}',auth=HTTPBasicAuth(username=username, password="jdsajdi"))
    assert response.status_code == 401
    
    
    response = client.get(f'/users/',auth=HTTPBasicAuth(username="hashdio", password=password))
    assert response.status_code == 401
    
    response = client.delete(f'/users/delete/{key}',auth=HTTPBasicAuth(username="ahui", password=password))
    assert response.status_code == 401

    # organisations
    
    response = client.delete(f'/users/delete/{key}',auth=HTTPBasicAuth(username=username, password=password))
    assert response.status_code == 200
    
def test_security():
    
    user1 = UserCreate(name="test1",
                       email=username,
                       password=password,
                       organisations=[])

    
    user2 = UserCreate(name="test2",
                       email=username2,
                       password=password2,
                       organisations=[])
    
    response = client.post('/users/add', data=user1.json(), auth=HTTPBasicAuth(username=username, password=password))
    assert response.status_code == 200
    key= response.json()["key"]

    response = client.post('/users/add', data=user2.json(), auth=HTTPBasicAuth(username=username2, password=password2))
    assert response.status_code == 200
    
    response = client.delete(f'/users/delete/{key}',auth=HTTPBasicAuth(username=username2, password=password2))
    assert response.status_code == 401


    response = client.get("/admin/delete_all", auth=HTTPBasicAuth(username=username, password=password))
    assert response.status_code == 401

    response = client.get("/admin/delete_all", auth=HTTPBasicAuth(username="admin", password="shdfhiuws"))
    assert response.status_code == 200
    
