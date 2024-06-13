import bcrypt

from ..injector import declare
from ..service import Service


@declare
class CryptographyService(Service):
    """Cryptography service"""

    def get_hashed_password(self, password: str) -> str:
        """Hash a password"""
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()

    def check_password(self, password: str, hashed_password: str) -> bool:
        """Check hashed password"""
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
