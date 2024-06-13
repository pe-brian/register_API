from unittest.mock import patch, MagicMock

from src.services.code_sender_service import CodeSenderService
from src.models.activation_code import ActivationCode
from src.models.user import User


class TestCodeSenderService:
    @patch("src.models.user.User.get")
    def test_send_activation_code(self, mock_user_get):
        with patch.object(
            CodeSenderService, "dispatch_service", MagicMock()
        ) as mock_dispatch:
            with patch.object(
                CodeSenderService, "smtp_service", MagicMock()
            ) as mock_smtp:
                mock_user = MagicMock(spec=User)
                mock_user.email = "test@example.com"
                mock_user_get.return_value = mock_user
                mock_activation_code = MagicMock(spec=ActivationCode)
                mock_activation_code.code = "123456"
                mock_activation_code.user_id = mock_user.id
                code_sender_service = CodeSenderService()
                code_sender_service.send_activation_code(mock_activation_code)
                mock_smtp.send_email.assert_called_once_with(
                    "Activation code", "123456", to_emails=[mock_user.email]
                )
                mock_dispatch.dispatch.assert_called_once_with(
                    "ACTIVATION_CODE_SENT",
                    code=mock_activation_code.code,
                    user_id=mock_user.id,
                )
