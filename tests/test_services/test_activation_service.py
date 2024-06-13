import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

from src.services.activation_service import (
    ActivationService,
    CodeExpiredError,
    WrongCodeError,
)


class TestActivationService:
    @pytest.fixture
    def user_mock(self):
        user = MagicMock()
        user.id = 1
        user.is_active = False
        return user

    @pytest.fixture
    def activation_code_mock(self):
        activation_code = MagicMock()
        activation_code.code = "1234"
        activation_code.timestamp = datetime.now().timestamp()
        activation_code.user_id = 1
        return activation_code

    @pytest.fixture
    def expired_activation_code_mock(self):
        activation_code = MagicMock()
        activation_code.code = "1234"
        activation_code.timestamp = (datetime.now() - timedelta(minutes=2)).timestamp()
        activation_code.user_id = 1
        return activation_code

    def test_has_code_expired_false(self, activation_code_mock: MagicMock):
        service = ActivationService()
        assert not service.has_code_expired(activation_code_mock.timestamp)

    def test_has_code_expired_true(self, expired_activation_code_mock: MagicMock):
        service = ActivationService()
        assert service.has_code_expired(expired_activation_code_mock.timestamp)

    @patch("src.services.activation_service.ActivationCode.get")
    def test_activate_correct_code(
        self, mock_get, user_mock: MagicMock, activation_code_mock: MagicMock
    ):
        mock_get.return_value = activation_code_mock
        with patch.object(
            ActivationService, "dispatch_service", MagicMock()
        ) as mock_dispatch:
            service = ActivationService()
            service.activate(user_mock, "1234")
            mock_dispatch.dispatch.assert_called_once_with(
                "USER_ACCOUNT_ACTIVATED", id=user_mock.id
            )
            assert user_mock.is_active

    @patch("src.services.activation_service.ActivationCode.get")
    def test_activate_incorrect_code(
        self, mock_get, user_mock: MagicMock, activation_code_mock: MagicMock
    ):
        mock_get.return_value = activation_code_mock
        service = ActivationService()
        with pytest.raises(WrongCodeError):
            service.activate(user_mock, "wrong_code")

    @patch("src.services.activation_service.ActivationCode.get")
    def test_activate_expired_code(
        self, mock_get, user_mock: MagicMock, expired_activation_code_mock: MagicMock
    ):
        mock_get.return_value = expired_activation_code_mock
        service = ActivationService()
        with pytest.raises(CodeExpiredError):
            service.activate(user_mock, "1234")
