import pytest
from src.models.user import User
from src.service import Service
from src.services.in_memory_database_service import InMemoryDatabaseService


@pytest.fixture
def db_service():
    return InMemoryDatabaseService()


@pytest.fixture(autouse=True)
def create_user_table(db_service: Service):
    db_service.register_models(User)
    db_service.create_table("user")


def test_create_object(db_service: Service):
    # Create a new user
    user_data = {"email": "alice@example.com", "password_hash": "*" * 60}
    user = db_service.create_object("user", **user_data)
    # Retrieve the user by ID
    retrieved_user = db_service.get_object_by_id("user", user.id)
    assert retrieved_user.email == "alice@example.com"
    assert retrieved_user.password_hash == "*" * 60


def test_update_object(db_service: Service):
    # Create a new user
    user_data = {"email": "bob@example.com", "password_hash": "*" * 60}
    user = db_service.create_object("user", **user_data)
    # Update user's email
    updated_user = db_service.update_object(
        "user", id=user.id, email="new_email@example.com"
    )
    assert updated_user.email == "new_email@example.com"


def test_delete_object_by_id(db_service: Service):
    # Create a new user
    user_data = {"email": "charlie@example.com", "password_hash": "*" * 60}
    user = db_service.create_object("user", **user_data)
    # Delete the user
    db_service.delete_object_by_id("user", user.id)
    with pytest.raises(IndexError):
        db_service.get_object_by_id("user", user.id)  # Should raise an IndexError
