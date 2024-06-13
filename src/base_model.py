from typing import Any, Iterable
from chocolatine import Condition, Col

from dataclasses import asdict, dataclass, field, fields

from src.service import Service
from .injector import inject
from .utils import camel_to_snake


class ModelFieldValidationError(Exception):
    def __init__(self, field: str, value: Any) -> None:
        super().__init__(f"Incorrect value {value} for field {field}")


@dataclass
@inject("DatabaseService")
class BaseModel:
    """Base model"""

    id: int = field(default=None, init=False)

    def __post_init__(self) -> None:
        for field in fields(self):
            value = getattr(self, field.name)
            if isinstance(value, int) and field.type == bool:
                setattr(self, field.name, bool(value))
        for key in vars(self):
            validator_name = f"validate_{key}"
            if hasattr(self, validator_name):
                validate = getattr(self, validator_name)
                if hasattr(validate, "__call__"):
                    validate()

    @classmethod
    def get_table_name(cls) -> str:
        """Return the table name"""
        return camel_to_snake(cls.__name__)

    @classmethod
    def create(cls, *args, **kwargs) -> object:
        """"""
        return Service.get("DatabaseService").create_object(
            table_name=cls.get_table_name(), *args, **kwargs
        )

    def save(self) -> object:
        """Save object to its table"""
        obj = self.database_service.create_or_update_object(
            table_name=self.__class__.get_table_name(), **asdict(self)
        )
        self.id = obj.id
        return obj

    def delete(self) -> None:
        """Remove object from its table"""
        self.database_service.delete_object_by_id(
            table_name=self.__class__.get_table_name(), id=self.id
        )
        self.id = None

    @classmethod
    def get(cls, id: int) -> object:
        """Get the first object matching the condition"""
        return Service.get("DatabaseService").get_object_by_id(cls.get_table_name(), id)

    @classmethod
    def filter(cls, condition: Condition) -> Iterable[object]:
        """Filter objects"""
        return Service.get("DatabaseService").filter_objects(
            table_name=cls.get_table_name(), condition=condition
        )
