from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import getenv
import smtplib
from typing import Iterable

from ..injector import declare, inject
from ..service import Service, ServiceNotAvailableError


@declare
@inject("DispatchService")
class SMTPService(Service):
    """SMTP service"""

    def __init__(self) -> None:
        self._host = getenv("SMTP_HOST")
        self._port = getenv("SMTP_PORT")
        self._username = getenv("SMTP_USERNAME")
        self._password = getenv("SMTP_PASSWORD")
        self._initialized = False
        if self._host and self._port and self._username and self._password:
            self._initialized = True

    def send_email(self, subject: str, body: str, to_emails: Iterable[str]) -> None:
        """Send an email"""
        # Check if the service is correctly initialized
        if not self._initialized:
            raise ServiceNotAvailableError("SMTPService")
        # Message creation
        msg = MIMEMultipart()
        msg["From"] = self._username
        msg["To"] = ", ".join(to_emails)
        msg["Subject"] = subject

        # Add the body
        msg.attach(MIMEText(body, "plain"))

        # Connect to the server and send the email
        with smtplib.SMTP(self._host, self._port) as server:
            server.ehlo()
            server.starttls()
            server.login(self._username, self._password)
            server.sendmail(self._username, to_emails, msg.as_string())
            server.close()

            self.dispatch_service.dispatch(
                "EMAIL_SENT", subject=subject, to_emails=to_emails
            )
