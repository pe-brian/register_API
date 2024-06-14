import pytest
from chocolatine import Col
from src.injector import Injector
from src.models.activation_code import ActivationCode
from src.models.user import User
from src.services.in_memory_database_service import InMemoryDatabaseService


@pytest.fixture(autouse=True)
def init():
    Injector.dependencies["DatabaseService"].cls = InMemoryDatabaseService
    db_service = Injector.resolve("DatabaseService")
    db_service.register_models(User, ActivationCode)
    db_service.create_tables()
    dispatch_service = Injector.resolve("DispatchService")
    for dep in Injector.dependencies.values():
        dispatch_service.subscribe(dep.get())


def test_end_to_end():
    user = User.register("test@test.com", "Password123!")
    code = ActivationCode.filter(Col("user_id") == user.id)[0]
    assert not user.is_active
    user.activate(code.code)
    assert user.is_active
