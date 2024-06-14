import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

from src.injector import Injector
from src.service import Service


@pytest.fixture(autouse=True)
def mock_dependencies():
    # Replace dependencies by mocks
    for name in Injector.dependencies:
        if name != "ActivationService":
            dep = Injector.dependencies[name]
            dep.cls = MagicMock()
            dep.cls.__name__ = name


@pytest.fixture
def user_mock():
    user = MagicMock()
    user.id = 1
    user.is_active = False
    return user


@pytest.fixture
def activation_code_mock():
    activation_code = MagicMock()
    activation_code.code = "1234"
    activation_code.timestamp = datetime.now().timestamp()
    activation_code.user_id = 1
    return activation_code


@pytest.fixture
def expired_activation_code_mock():
    activation_code = MagicMock()
    activation_code.code = "1234"
    activation_code.timestamp = (datetime.now() - timedelta(minutes=2)).timestamp()
    activation_code.user_id = 1
    return activation_code


def test_has_code_expired_false(activation_code_mock: MagicMock):
    service = Service.get("ActivationService")
    assert not service.has_code_expired(activation_code_mock.timestamp)


def test_has_code_expired_true(expired_activation_code_mock: MagicMock):
    service = Service.get("ActivationService")
    assert service.has_code_expired(expired_activation_code_mock.timestamp)


@patch("src.services.activation_service.ActivationCode.get")
def test_activate_correct_code(
    mock_get: MagicMock, user_mock: MagicMock, activation_code_mock: MagicMock
):
    mock_get.return_value = activation_code_mock
    
    service = Service.get("ActivationService")
    service.activate(user_mock, "1234")
    Service.get("DispatchService").dispatch.assert_called_once_with(
        "USER_ACCOUNT_ACTIVATED", id=user_mock.id
    )
    assert user_mock.is_active


@patch("src.services.activation_service.ActivationCode.get")
def test_activate_incorrect_code(
    mock_get: MagicMock, user_mock: MagicMock, activation_code_mock: MagicMock
):
    mock_get.return_value = activation_code_mock
    service = Service.get("ActivationService")
    with pytest.raises(PermissionError, match="Wrong code"):
        service.activate(user_mock, "wrong_code")


@patch("src.services.activation_service.ActivationCode.get")
def test_activate_expired_code(
    mock_get: MagicMock, user_mock: MagicMock, expired_activation_code_mock: MagicMock
):
    mock_get.return_value = expired_activation_code_mock
    service = Service.get("ActivationService")
    with pytest.raises(PermissionError, match="Code expired"):
        service.activate(user_mock, "1234")


@patch("src.services.activation_service.ActivationCode.get")
def test_activate_user_is_already_active(
    mock_get: MagicMock, user_mock: MagicMock, expired_activation_code_mock: MagicMock
):
    user_mock.is_active = True
    mock_get.return_value = expired_activation_code_mock
    service = Service.get("ActivationService")
    with pytest.raises(PermissionError, match="User is already active"):
        service.activate(user_mock, "1234")
