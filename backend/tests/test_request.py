import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

#Test /request without email - should return token, not save
def test_request_without_email(sample_request_data):
    response = client.post("/api/request", json=sample_request_data)

    assert response.status_code == 200
    data = response.json()

    # Should not be saved
    assert data["saved"] == False
    # Should have a token
    assert "draft_token" in data
    assert data["draft_token"] is not None
    assert len(data["draft_token"]) > 0
    # Should have answer
    assert "answer_text" in data
    assert data["answer_text"] is not None

#Test /request with email - should save, no token
def test_request_with_email(sample_request_with_email):
    response = client.post("/api/request", json=sample_request_with_email)

    assert response.status_code == 200
    data = response.json()

    # Should be saved
    assert data["saved"] == True
    # Should NOT have a token (or token should be None)
    assert data.get("draft_token") is None
    # Should have answer
    assert "answer_text" in data

#Test /request with missing required fields
def test_request_invalid_data():
    invalid_data = {
        "dob": "1990-01-15"
        # Missing birth_time, birth_location, etc.
    }

    response = client.post("/api/request", json=invalid_data)

    # Should return validation error (422)
    assert response.status_code == 422

def test_request_with_partial_data(sample_request_data):
    """Test /request with optional fields missing"""
    # Remove optional fields
    del sample_request_data["substance"]
    del sample_request_data["intention"]

    response = client.post("/api/request", json=sample_request_data)

    # Should still work
    assert response.status_code == 200
