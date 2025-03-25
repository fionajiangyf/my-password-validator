# test_main.py
import pytest
from main import app

@pytest.fixture
def client():
    """
    Pytest fixture that creates a Flask test client from the 'app' in main.py.
    """
    with app.test_client() as client:
        yield client

def test_root_endpoint(client):
    """
    Test the GET '/' endpoint to ensure it returns
    the greeting and a 200 status code.
    """
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Hello from my Password Validator!" in resp.data

def test_check_password_valid(client):
    """
    Test a valid password that meets all criteria.
    """
    resp = client.post("/v1/checkPassword", json={"password": "Valid1!@"})
    data = resp.get_json()
    assert resp.status_code == 200
    assert data["valid"] is True
    assert data["reason"] == ""

def test_check_password_too_short(client):
    """
    Test a password that is too short.
    """
    resp = client.post("/v1/checkPassword", json={"password": "V1!a"})
    data = resp.get_json()
    assert resp.status_code == 200
    assert data["valid"] is False
    assert "at least 8 characters" in data["reason"]

def test_check_password_missing_uppercase(client):
    """
    Test a password with no uppercase letter.
    """
    resp = client.post("/v1/checkPassword", json={"password": "valid1!@"})
    data = resp.get_json()
    assert resp.status_code == 200
    assert data["valid"] is False
    assert "uppercase" in data["reason"]

def test_check_password_missing_digit(client):
    """
    Test a password with no digit.
    """
    resp = client.post("/v1/checkPassword", json={"password": "Valid!@#"})
    data = resp.get_json()
    assert resp.status_code == 200
    assert data["valid"] is False
    assert "digit" in data["reason"]

def test_check_password_missing_special_char(client):
    """
    Test a password with no special character.
    """
    resp = client.post("/v1/checkPassword", json={"password": "Valid123"})
    data = resp.get_json()
    assert resp.status_code == 200
    assert data["valid"] is False
    assert "special character" in data["reason"]
