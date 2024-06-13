from ..models.activation_code import ActivationCode
from ..models.user import User
from ..injector import declare, inject
from ..service import Service, ServiceNotAvailableError


@declare
@inject("SMTPService")
@inject("DispatchService")
class CodeSenderService(Service):
    """ Code sender service """
    def __init__(self) -> None:
        self._method = "email"
        super().__init__()

    def send_activation_code(self, activation_code: ActivationCode) -> None:
        """ Send activation code """
        user = User.get(id=activation_code.user_id)
        try:
            self.smtp_service.send_email("Activation code", activation_code.code, to_emails=[user.email])
        except ServiceNotAvailableError:
            self.dispatch_service.dispatch("ERROR_SMTP_SERVICE_NOT_AVAILABLE")
            self.dispatch_service.dispatch("ERROR_ACTIVATION_CODE_NOT_SENT", code=activation_code.code, user_id=user.id)
        else:
            self.dispatch_service.dispatch("ACTIVATION_CODE_SENT", code=activation_code.code, user_id=user.id)
