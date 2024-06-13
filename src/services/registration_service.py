from ..models.activation_code import ActivationCode
from ..models.user import User
from ..injector import declare, inject
from ..service import Service


class UserAlreadyRegisteredError(Exception):
    def __init__(self, email: str) -> None:
        super().__init__(f"User already registered with email {email}")


@declare
@inject("DispatchService")
@inject("CodeSenderService")
class RegistrationService(Service):
    """ Registration service """
    def register(self, email: str, password: str) -> User:
        """ Register a user with email and password """
        # Raise an error if user already registered
        if User.get_by_email(email):
            raise UserAlreadyRegisteredError(email)
        # Create user
        user = User.create(email=email, password=password)
        user.save()
        self.dispatch_service.dispatch("USER_REGISTERED", id=user.id)
        # Create activation code
        activation_code = ActivationCode.create(user_id=user.id)
        activation_code.save()
        self.dispatch_service.dispatch("ACTIVATION_CODE_CREATED", id=activation_code.id)
        # Send activation code
        self.code_sender_service.send_activation_code(activation_code)

        return user
