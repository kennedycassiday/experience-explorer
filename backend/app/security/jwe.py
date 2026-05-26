import json
from jwcrypto import jwk, jwe
from jwcrypto.common import json_encode
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone

# Store the encryption key (don’t regenerate it each time)
# Encrypt function, create a token from RequestIn + answer_text
# Decrypt function, read the token to get the original data
# Integration,  use it in /request (when no email) and /save (to decrypt)

# 1. User requests WITHOUT email
#    → Generate answer
#    → Encrypt RequestIn + answer_text into JWE token
#    → Return AnswerOut with draft_token

# 2. User decides to save later
#    → Send EmailOptIn with draft_token + email
#    → Decrypt token to get original RequestIn + answer_text
#    → Create User + Experience and save
load_dotenv()
TOKEN_TTL_HOURS = 24

def get_key():
    key = jwk.JWK.from_json(os.environ["JWE_KEY_CURRENT"])
    return key

def create_token(request_data, answer_text):
    key = get_key()

    # prep payload
    expires_at = datetime.now(timezone.utc) + timedelta(hours=TOKEN_TTL_HOURS)

    payload = {
        "request": request_data,
        "answer_text": answer_text,
        "expires_at": expires_at.isoformat(),  # store as ISO 8601 string
    }

    payload_json = json.dumps(payload)

    protected_header = {
        "alg": "dir",
        "enc": "A256GCM",
    }

    token = jwe.JWE(
        payload_json.encode("utf-8"),
        recipient=key,
        protected=protected_header,
    )

    return token.serialize(compact=True)

def decrypt_token(jwetoken):
    key = get_key()

    try:
        token = jwe.JWE()
        token.deserialize(jwetoken, key=key)

        payload = token.payload.decode("utf-8")
        data = json.loads(payload)

        # Check expiration
        expires_at_str = data.get("expires_at")
        if not expires_at_str:
            raise ValueError("Token missing expires_at")

        expires_at = datetime.fromisoformat(expires_at_str)
        now = datetime.now(timezone.utc)

        if expires_at < now:
            raise ValueError("Token has expired")

        return data

    except Exception as e:
        raise ValueError(f"Invalid or expired token: {str(e)}")



#test script
if __name__ == "__main__":
    from datetime import date, time

    # First, generate a key if you don't have one
    if "JWE_KEY_CURRENT" not in os.environ:
        print("Generating new key...")
        key = jwk.JWK.generate(kty='oct', size=256)
        key_json = key.export()
        print(f"\nAdd this to your environment variable JWE_KEY_CURRENT:")
        print(key_json)
        print("\nOr set it temporarily for this test:")
        os.environ["JWE_KEY_CURRENT"] = key_json

    # Test data (simulating RequestIn)
    test_request = {
        "name": "Test User",
        "email": None,
        "dob": "1990-01-15",  # date as string for JSON
        "birth_time": "14:30:00",  # time as string for JSON
        "birth_location": "New York",
        "experience_date": "2024-01-20",
        "experience_time": "20:00:00",
        "experience_location": "California",
        "substance": "Test substance",
        "intention": "Test intention"
    }

    test_answer = "This is a test answer"

    print("\n=== Testing JWE Encryption/Decryption ===\n")

    # Test encryption
    print("1. Creating token...")
    try:
        token = create_token(test_request, test_answer)
        print(f"   ✓ Token created: {token[:50]}...")
    except Exception as e:
        print(f"   ✗ Error creating token: {e}")
        exit(1)

    # Test decryption
    print("\n2. Decrypting token...")
    try:
        decrypted = decrypt_token(token)
        print(f"   ✓ Token decrypted successfully")
        print(f"   Answer text: {decrypted['answer_text']}")
        print(f"   Request name: {decrypted['request']['name']}")
        print(f"   Request dob: {decrypted['request']['dob']}")
    except Exception as e:
        print(f"   ✗ Error decrypting token: {e}")
        exit(1)

    # Verify data matches
    print("\n3. Verifying data integrity...")
    if decrypted['answer_text'] == test_answer and decrypted['request']['name'] == test_request['name']:
        print("   ✓ All data matches! JWE is working correctly.")
    else:
        print("   ✗ Data mismatch!")

    print("\n=== Test Complete ===")
