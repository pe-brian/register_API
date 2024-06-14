from unittest.mock import MagicMock, patch
from flask.testing import FlaskClient
import pytest

from app import app
from src.service import Service
from tests.mocks.in_memory_database_service import DatabaseService
from src.models.activation_code import ActivationCode
from src.models.user import User


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def initialize_db():
    db_service = Service.get("DatabaseService")
    db_service.register_models(User, ActivationCode)
    db_service.create_tables()


def test_register(client: FlaskClient):
    response = client.post(
        "/register", json={"email": "test@example.com", "password": "Password123!"}
    )
    assert response.status_code == 200
    json_data = response.get_json()
    assert (
        json_data["message"]
        == "User registered, please check your email for the activation code"
    )


def test_activate(client: FlaskClient):
    with patch("app.User.get_by_email") as get_by_email_mock:
        user_mock = MagicMock(spec=User)
        get_by_email_mock.return_value = user_mock
        response = client.post(
            "/activate", json={"email": "test@example.com", "password": "Password123!", "code": "1234"}
        )
        assert user_mock.authenticate.called
        assert user_mock.activate.called
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data["message"] == "User activated"
