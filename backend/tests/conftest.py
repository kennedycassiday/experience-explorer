# Shared fixtures and test setup
import pytest
import os
from pathlib import Path
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from app.main import app
from app.db import create_db_and_tables


# Ensure database exists before tests
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create database if it doesn't exist"""
    db_path = Path("experience.db")
    if not db_path.exists():
        # Create the database and tables
        create_db_and_tables()
    yield

# Test client that uses test database
@pytest.fixture(scope="function")
def client(test_db):
    # Override the app's database engine with test database
    app.dependency_overrides = {}
    # May need to create a dependency override for get_session
    # For now, patching it in individual tests if needed

    with TestClient(app) as test_client:
        yield test_client

# Sample test data
@pytest.fixture
def sample_request_data():
    return {
        "dob": "1990-01-15",
        "birth_time": "14:30:00",
        "birth_location": "New York, New York",
        "experience_date": "2026-02-20",
        "experience_time": "20:00:00",
        "experience_location": "Los Angeles, California",
        "substance": "MDMA",
        "intention": "To release grief"
    }

@pytest.fixture
def sample_request_with_email():
    return {
        "name": "Jane Doe",
        "email": "jane@doe.com",
        "dob": "1990-01-15",
        "birth_time": "14:30:00",
        "birth_location": "New York, New York",
        "experience_date": "2026-02-20",
        "experience_time": "20:00:00",
        "experience_location": "Los Angeles, California"
    }
