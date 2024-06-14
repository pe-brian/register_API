import pytest

from chocolatine import Col

from src.injector import Injector
from src.models.activation_code import ActivationCode
from src.models.user import User


@pytest.fixture(autouse=True)
def prepare_db():
    db_service = Injector.resolve("DatabaseService")
    db_service.register_models(User, ActivationCode)
    db_service.create_tables()


@pytest.fixture(autouse=True)
def subscribe_to_dispatch_service():
    dispatch_service = Injector.resolve("DispatchService")
    for dep in Injector.dependencies.values():
        dispatch_service.subscribe(dep.get())


def test_end_to_end():
    print(Injector.dependencies)
    user = User.register("test@test.com", "Password123!")
    code = ActivationCode.filter(Col("user_id") == user.id)[0]
    assert not user.is_active
    user.activate(code.code)
    assert user.is_active
