from unittest.mock import patch, MagicMock

from src.services.smtp_service import SMTPService


class TestSMTPService:
    @patch(
        "src.services.smtp_service.getenv",
        side_effect=lambda k: {
            "SMTP_HOST": "smtp.example.com",
            "SMTP_PORT": "587",
            "SMTP_USERNAME": "user@example.com",
            "SMTP_PASSWORD": "password",
        }[k],
    )
    @patch("src.services.smtp_service.smtplib.SMTP")
    def test_send_email(self, mock_smtp, mock_getenv):
        with patch.object(
            SMTPService, "dispatch_service", MagicMock()
        ) as mock_dispatch:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server
            smtp_service = SMTPService()
            smtp_service.send_email(
                "Test Subject", "Test Body", ["recipient@example.com"]
            )
            mock_server.ehlo.assert_called_once()
            mock_server.starttls.assert_called_once()
            mock_server.login.assert_called_once_with("user@example.com", "password")
            mock_server.sendmail.assert_called_once_with(
                "user@example.com",
                ["recipient@example.com"],
                mock_server.sendmail.call_args[0][2],
            )
            mock_dispatch.dispatch.assert_called_once_with(
                "EMAIL_SENT",
                subject="Test Subject",
                to_emails=["recipient@example.com"],
            )
