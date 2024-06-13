from unittest.mock import patch, MagicMock

from src.services.registration_service import RegistrationService
from src.models.user import User
from src.models.activation_code import ActivationCode

class TestRegistrationService:
    @patch('src.models.user.User.create')
    @patch('src.models.activation_code.ActivationCode.create')
    def test_register(self, mock_activation_code_create: MagicMock, mock_user_create: MagicMock):
        with patch.object(RegistrationService, 'dispatch_service', MagicMock()) as mock_dispatch,\
             patch.object(RegistrationService, 'code_sender_service', MagicMock()) as mock_code_sender:
            mock_user = MagicMock(spec=User)
            mock_activation_code = MagicMock(spec=ActivationCode)
            mock_user_create.return_value = mock_user
            mock_activation_code_create.return_value = mock_activation_code
            registration_service = RegistrationService()
            user = registration_service.register('test@example.com', 'password123')
            mock_user_create.assert_called_once_with(email='test@example.com', password='password123')
            mock_user.save.assert_called_once()
            mock_code_sender.send_activation_code.assert_called_once()
            mock_activation_code_create.assert_called_once_with(user_id=mock_user.id)
            mock_activation_code.save.assert_called_once()
            mock_dispatch.dispatch.assert_any_call("USER_REGISTERED", id=mock_user.id)
            mock_dispatch.dispatch.assert_any_call("ACTIVATION_CODE_CREATED", id=mock_activation_code.id)
            assert user == mock_user
