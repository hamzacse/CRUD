from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_note():
    response = client.post("/notes/", json={"title": "Test", "content": "Hello"})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test"


def test_read_note():
    client.post("/notes/", json={"title": "ReadMe", "content": "World"})
    response = client.get("/notes/2")
    assert response.status_code == 200
    assert response.json()["title"] == "ReadMe"


def test_update_note():
    client.post("/notes/", json={"title": "Old", "content": "content"})
    response = client.put("/notes/3", json={"title": "New", "content": "Updated"})
    assert response.status_code == 200
    assert response.json()["title"] == "New"


def test_delete_note():
    client.post("/notes/", json={"title": "Delete", "content": "Me"})
    response = client.delete("/notes/4")
    assert response.status_code == 200

    response = client.get("/notes/4")
    assert response.status_code == 404