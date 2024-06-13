from dataclasses import dataclass, field
from datetime import datetime
from typing import Self

from ..base_model import BaseModel, ModelFieldValidationError
from ..injector import inject
from ..utils import generate_code


@dataclass
@inject("ValidationService")
class ActivationCode(BaseModel):
    """Activation code model"""

    user_id: int
    code: str = field(default_factory=generate_code)
    timestamp: float = field(default_factory=datetime.now().timestamp)

    def validate_code(self) -> None:
        """Validate the code"""
        if self.code and self.validation_service.is_valid_code_format(self.code):
            return
        raise ModelFieldValidationError()

    def validate_user_id(self) -> None:
        """Validate the user id"""
        if self.user_id and self.validation_service.is_valid_user_id_format(
            self.user_id
        ):
            return
        raise ModelFieldValidationError()

    @staticmethod
    def create(user_id: int) -> Self:
        """Create an activation code"""
        return ActivationCode(user_id=user_id)
