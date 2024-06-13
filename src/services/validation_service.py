import re

from ..injector import declare
from ..service import Service


@declare
class ValidationService(Service):
    """Validation service"""

    def is_valid_email_format(self, email: str) -> bool:
        """Check is an email is valid"""
        return bool(re.match(r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+(\.\w+)?$", email))

    def is_valid_code_format(self, code: str) -> bool:
        """Check is a code format is valid"""
        return bool(re.fullmatch(r"\d{4}", code))

    def is_valid_password_hash_format(self, password_hash: str) -> bool:
        """Check if the password hash has a correct format"""
        return len(password_hash) == 60

    def is_valid_user_id_format(self, user_id: int) -> bool:
        """Check if the user id has a correct value"""
        return user_id >= 0

    def is_valid_password_format(self, password: str) -> bool:
        """Check if the password has a correct format"""
        if len(password) < 8:
            return False
        if not any(char.isdigit() for char in password):
            return False
        if not any(char.isupper() for char in password):
            return False
        if not any(char.islower() for char in password):
            return False
        if not any(char in "!@#$%^&*()-+?_=,<>/" for char in password):
            return False
        return True
