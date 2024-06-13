import pytest
from src.services.validation_service import ValidationService


validation_service = ValidationService()


@pytest.mark.parametrize(
    "email, expected",
    [
        ("test@example.com", True),
        ("invalid-email.com", False),
        ("user@domain.co.uk", True),
        ("user.name@domain.com", True),
        ("user_name@domain.com", True),
        ("user@domain", False),
        ("@domain.com", False),
        ("user@", False),
        ("", False),
    ],
)
def test_is_valid_email_format(email: str, expected: bool):
    assert validation_service.is_valid_email_format(email) == expected


@pytest.mark.parametrize(
    "code, expected",
    [
        ("1234", True),
        ("1a2b", False),
        ("123", False),
        ("12345", False),
        ("abcd", False),
        ("", False),
    ],
)
def test_is_valid_code_format(code: str, expected: bool):
    assert validation_service.is_valid_code_format(code) == expected


@pytest.mark.parametrize(
    "password_hash, expected",
    [("a" * 60, True), ("a" * 59, False), ("a" * 61, False), ("", False)],
)
def test_is_valid_password_hash_format(password_hash: int, expected: bool):
    assert validation_service.is_valid_password_hash_format(password_hash) == expected


@pytest.mark.parametrize(
    "user_id, expected", [(0, True), (1, True), (-1, False), (100, True), (-100, False)]
)
def test_is_valid_user_id_format(user_id: int, expected: bool):
    assert validation_service.is_valid_user_id_format(user_id) == expected


@pytest.mark.parametrize(
    "password, expected",
    [
        ("Password1!", True),
        ("pass1!", False),  # Too short
        ("PASSWORD1!", False),  # No lower case
        ("password1!", False),  # No up case
        ("Password!", False),  # No number
        ("Password1", False),  # No special character
        ("", False),  # Empty
    ],
)
def test_is_valid_password_format(password: str, expected: bool):
    assert validation_service.is_valid_password_format(password) == expected
