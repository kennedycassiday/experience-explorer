import pytest
from app.security.jwe import create_token, decrypt_token

#Test that token creation works
def test_create_token():
    request_data = {
        "dob": "1990-01-15",
        "birth_time": "14:30:00",
        "birth_location": "New York, New York"
    }
    answer_text = "Expect strong transformative energy (Pluto–Venus aspect): deep emotional renewal, potential catharsis around relationships."

    token = create_token(request_data, answer_text)

    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0

#Test that token decryption works
def test_decrypt_token():
    request_data = {
        "dob": "1990-01-15",
        "birth_time": "14:30:00",
        "birth_location": "New York, New York"
    }
    answer_text = "Expect strong transformative energy (Pluto–Venus aspect): deep emotional renewal, potential catharsis around relationships."

    token = create_token(request_data, answer_text)
    decrypted = decrypt_token(token)

    assert decrypted["answer_text"] == answer_text
    assert decrypted["request"]["dob"] == request_data["dob"]
    assert decrypted["request"]["birth_location"] == request_data["birth_location"]

def test_create_and_decrypt_roundtrip():
    """Test full roundtrip: create → decrypt → verify"""
    original_request = {
        "name": "Test User",
        "email": None,
        "dob": "1990-01-15",
        "birth_time": "14:30:00",
        "birth_location": "New York",
        "experience_date": "2024-01-20",
        "experience_time": "20:00:00",
        "experience_location": "California",
        "substance": "Test substance",
        "intention": "Test intention"
    }
    original_answer = "This is a test answer"

    # Create token
    token = create_token(original_request, original_answer)

    # Decrypt token
    decrypted = decrypt_token(token)

    # Verify all data matches
    assert decrypted["answer_text"] == original_answer
    assert decrypted["request"]["dob"] == original_request["dob"]
    assert decrypted["request"]["birth_time"] == original_request["birth_time"]
    assert decrypted["request"]["birth_location"] == original_request["birth_location"]
    assert decrypted["request"]["experience_date"] == original_request["experience_date"]
    assert decrypted["request"]["substance"] == original_request["substance"]

def test_decrypt_invalid_token():
    """Test that invalid token raises ValueError"""
    with pytest.raises(ValueError):
        decrypt_token("not-a-valid-token")

    with pytest.raises(ValueError):
        decrypt_token("eyJ.invalid.token")
