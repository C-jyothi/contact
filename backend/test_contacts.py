
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base, get_db


# Create a separate temporary test database.
TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


# Provide the test database to the APIs.
def override_get_db():

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


# Run before each test.
@pytest.fixture
def client():

    Base.metadata.create_all(bind=test_engine)

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

    Base.metadata.drop_all(bind=test_engine)


# Test 1: Add a contact.
def test_add_contact(client):

    response = client.post(
        "/contacts",
        json={
            "name": "Rahul",
            "email": "rahul@gmail.com",
            "phone": "9876543210"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Rahul"
    assert data["email"] == "rahul@gmail.com"


# Test 2: Get all contacts.
def test_get_contacts(client):

    client.post(
        "/contacts",
        json={
            "name": "Anu",
            "email": "anu@gmail.com",
            "phone": "9876543211"
        }
    )

    response = client.get("/contacts")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

    assert data[0]["name"] == "Anu"


# Test 3: Delete a contact.
def test_delete_contact(client):

    add_response = client.post(
        "/contacts",
        json={
            "name": "Meera",
            "email": "meera@gmail.com",
            "phone": "9876543212"
        }
    )

    contact_id = add_response.json()["id"]

    delete_response = client.delete(
        f"/contacts/{contact_id}"
    )

    assert delete_response.status_code == 200

    get_response = client.get("/contacts")

    assert len(get_response.json()) == 0
