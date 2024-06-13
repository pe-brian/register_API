from datetime import datetime, timedelta

from chocolatine import Col

from ..injector import declare, inject
from ..models.activation_code import ActivationCode
from ..models.user import User
from ..service import Service


class CodeExpiredError(Exception):
    def __init__(self) -> None:
        super().__init__("Code has expired")


class WrongCodeError(Exception):
    def __init__(self) -> None:
        super().__init__("Wrong code")


class UserAlreadyActivatedError(Exception):
    def __init__(self, email: str) -> None:
        super().__init__(f"User already activated with email {email}")


@declare
@inject("DispatchService")
class ActivationService(Service):
    """ Activation service """
    def has_code_expired(self, code_timestamp: float) -> bool:
        """ Check if the code has expired """
        return datetime.now() > datetime.fromtimestamp(code_timestamp) + timedelta(minutes=1)

    def activate(self, user: User, code: str) -> None:
        """ Activate the user account """
        if user.is_active:
            raise UserAlreadyActivatedError(user.email)
        activation_code = ActivationCode.get(user.id)
        if code != activation_code.code:
            raise WrongCodeError()
        if self.has_code_expired(activation_code.timestamp):
            activation_code.delete()
            raise CodeExpiredError()
        else:
            self.dispatch_service.dispatch("USER_ACCOUNT_ACTIVATED", id=user.id)
            user.is_active = True
            user.save()
