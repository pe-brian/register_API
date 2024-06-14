from unittest.mock import patch, MagicMock

import pytest
from src.injector import Injector

from src.service import Service

from src.models.user import User
from src.models.activation_code import ActivationCode


@pytest.fixture(autouse=True)
def mock_dependencies():
    # Replace dependencies by mocks
    for name in Injector.dependencies:
        if name != "RegistrationService":
            dep = Injector.dependencies[name]
            dep.cls = MagicMock()
            dep.cls.__name__ = name


@patch("src.models.user.User.create")
@patch("src.models.activation_code.ActivationCode.create")
def test_register(mock_activation_code_create: MagicMock, mock_user_create: MagicMock):
    mock_user = MagicMock(spec=User)
    mock_activation_code = MagicMock(spec=ActivationCode)
    mock_user_create.return_value = mock_user
    mock_activation_code.user_id = 1
    mock_activation_code.code = "1234"
    mock_activation_code_create.return_value = mock_activation_code
    Service.get("DatabaseService").filter_objects.return_value = []
    user = Service.get("RegistrationService").register(
        "test@example.com", "password123"
    )  # tested function call
    mock_user_create.assert_called_once_with(
        email="test@example.com", password="password123"
    )
    mock_user.save.assert_called_once()
    Service.get("CodeSenderService").send_activation_code.assert_called_once()
    mock_activation_code_create.assert_called_once_with(user_id=mock_user.id)
    mock_activation_code.save.assert_called_once()
    Service.get("DispatchService").dispatch.assert_any_call(
        "USER_REGISTERED", id=mock_user.id
    )
    Service.get("DispatchService").dispatch.assert_any_call(
        "ACTIVATION_CODE_CREATED", id=mock_activation_code.id
    )
    assert user == mock_user
