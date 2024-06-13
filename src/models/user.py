from dataclasses import dataclass, field
from datetime import datetime
from typing import Self

from chocolatine import Col

from ..service import Service
from ..injector import inject
from ..base_model import BaseModel, ModelFieldValidationError


class UserAuthenticationError(Exception):
    def __init__(self) -> None:
        super().__init__("Wrong password")


@dataclass
@inject("ValidationService")
@inject("ActivationService")
@inject("CryptographyService")
class User(BaseModel):
    """ User model """
    email: str
    password_hash: str
    is_active: bool = False
    signup_timestamp: float = field(default_factory=datetime.now().timestamp)
    
    @staticmethod
    @inject("CryptographyService")
    def create(cryptography_service: Service, email: str, password: str) -> Self:
        """ Create a user """
        password_hash = cryptography_service.get_hashed_password(password)
        return User(email=email, password_hash=password_hash)
    
    @staticmethod
    def register(email: str, password: str) -> Self:
        """ Register a user """
        return Service.get("RegistrationService").register(email=email, password=password)

    def validate_email(self) -> None:
        """ Validate email """
        if self.email and self.validation_service.is_valid_email_format(self.email):
            return
        raise ModelFieldValidationError()
    
    def validate_password_hash(self) -> None:
        """ Validate password hash """
        if self.password_hash and self.validation_service.is_valid_password_hash_format(self.password_hash):
            return
        raise ModelFieldValidationError()
    
    @staticmethod
    def get_by_email(email: str) -> Self:
        """ Get a user by email """
        res = User.filter(condition=(Col("email") == email))
        return res[0] if res else None

    def authenticate(self, password: str, check_password: str) -> None:
        """ Authenticate the user """
        if not self.cryptography_service.check_password(password, check_password):
            raise UserAuthenticationError()

    def activate(self, code: str) -> None:
        """ Activate the user """
        self.activation_service.activate(self, code)