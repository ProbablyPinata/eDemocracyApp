from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_sanity():
    response = client.post(
        "/users/add", json={"name": "test1", "email": "email1", "pw": "hello", "organisations": []}
    )
    assert response.status_code == 200
    assert response.json() == {"name": "test1", "email": "email1", "pw": "hello", "id": 1,"organisations": []}
    response = client.post(
        "/users/add", json={"name": "test2", "email": "email2", "pw": "hello", "organisations": []}
    )
    response = client.post(
        "/users/add", json={"name": "test3", "email": "email3", "pw": "hello", "organisations": []}
    )
    print("Passed user tests")

    response = client.get(
        '/users/name/1/'
    )
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {"name": "test1", "email": "email1", "pw": "hello", "id": 1,"organisations": []}

    response = client.get(
        '/users/'
    )
    assert response.status_code == 200
    assert {"name": "test2", "email": "email2", "pw": "hello", "id": 2,"organisations": []} in response.json()

