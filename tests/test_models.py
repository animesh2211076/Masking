import pytest
from pydantic import ValidationError

from models import UserCreate


def _valid_payload():
    return {
        "name": "Animesh Maurya",
        "phone": "9876543210",
        "email": "animesh@gmail.com",
        "pan": "ABCDE1234F",
        "ifsc": "SBIN0001234",
        "upi": "animesh@upi",
        "account": "123456789012",
        "balance": 5400.0,
    }


def test_user_create_valid():
    user = UserCreate(**_valid_payload())
    assert user.email == "animesh@gmail.com"
    assert user.balance == 5400.0


def test_user_create_invalid_phone():
    payload = _valid_payload()
    payload["phone"] = "12345"
    with pytest.raises(ValidationError):
        UserCreate(**payload)
