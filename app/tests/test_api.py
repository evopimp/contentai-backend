# backend/tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.content import Content
from app.models.user import User

client = TestClient(app)

@pytest.fixture
def test_content():
    return {
        "title": "Test Content",
        "description": "Test Description",
        "content_type": "article",
        "tags": ["test"]
    }

@pytest.fixture
def test_user():
    return {
        "email": "test@example.com",
        "username": "testuser"
    }

class TestContentAPI:
    def test_create_content(self, test_content):
        response = client.post("/api/v1/content/", json=test_content)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == test_content["title"]
        assert "_id" in data

    def test_get_content(self, test_content):
        # First create content
        create_response = client.post("/api/v1/content/", json=test_content)
        content_id = create_response.json()["_id"]

        # Then get it
        response = client.get(f"/api/v1/content/{content_id}")
        assert response.status_code == 200
        assert response.json()["title"] == test_content["title"]

    def test_list_contents(self, test_content):
        client.post("/api/v1/content/", json=test_content)
        response = client.get("/api/v1/content/")
        assert response.status_code == 200
        assert len(response.json()) > 0

class TestUserAPI:
    def test_create_user(self, test_user):
        response = client.post("/api/v1/users/", json=test_user)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user["email"]

    def test_duplicate_email(self, test_user):
        # Create first user
        client.post("/api/v1/users/", json=test_user)
        # Try to create duplicate
        response = client.post("/api/v1/users/", json=test_user)
        assert response.status_code == 400