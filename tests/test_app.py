from flask.testing import FlaskClient
import pytest


from app import app
from src.injector import Injector
from src.services.in_memory_database_service import InMemoryDatabaseService
from src.models.activation_code import ActivationCode
from src.models.user import User


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def mock_db_service():
    Injector.dependencies["DatabaseService"].cls = InMemoryDatabaseService
    db_service = Injector.resolve("DatabaseService")
    db_service.register_models(User, ActivationCode)
    db_service.create_tables()
    dispatch_service = Injector.resolve("DispatchService")
    dispatch_service.subscribe(Injector.dependencies.values())


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
    response = client.post(
        "/activate", json={"email": "test@example.com", "code": "1234"}
    )
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["message"] == "User activated"
