import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.security.jwe import create_token

client = TestClient(app)

#Test /save with a valid token from /request
def test_save_with_valid_token(sample_request_data):
    # First, get a token from /request
    request_response = client.post("/request", json=sample_request_data)
    assert request_response.status_code == 200
    token = request_response.json()["draft_token"]

    # Now use that token to save
    save_data = {
        "draft_token": token,
        "email": "test@example.com",
        "name": "Test User"
    }

    response = client.post("/save", json=save_data)

    assert response.status_code == 200
    data = response.json()

    # Should return SaveResult with IDs
    assert "user_id" in data
    assert "experience_id" in data
    assert data["user_id"] > 0
    assert data["experience_id"] > 0

#Test /save with invalid token
def test_save_invalid_token():
    save_data = {
        "draft_token": "not-a-valid-token",
        "email": "test@example.com"
    }

    response = client.post("/save", json=save_data)

    # Should return 400 Bad Request
    assert response.status_code == 400
    assert "Invalid token" in response.json()["detail"]

#Test /save without email
def test_save_missing_email():
    # Create a valid token first
    token = create_token(
        {"dob": "1990-01-15", "birth_time": "14:30:00", "birth_location": "NY"},
        "Test answer"
    )

    save_data = {
        "draft_token": token
        # Missing email
    }

    response = client.post("/save", json=save_data)

    # Should return validation error (422)
    assert response.status_code == 422
