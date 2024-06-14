from random import randint
import re
from typing import Union

from chocolatine import SqlType


def generate_code() -> str:
    """Generate a 4 digits code"""
    return "".join(str(randint(0, 9)) for _ in range(4))


def camel_to_snake(name: str) -> str:
    """Convert a string from camel case to snake case"""
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub("__([A-Z])", r"_\1", name)
    name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name)
    return name.lower()


def cast_to_sql_type(old_type: Union[str, int, float]) -> SqlType:
    """Cast an old type to a Chocolatine SqlType"""
    match old_type.__name__:
        case "str":
            return SqlType.String
        case "int":
            return SqlType.Integer
        case "float":
            return SqlType.Float
        case "bool":
            return SqlType.Boolean
        case _:
            raise ValueError("Incompatible type")

