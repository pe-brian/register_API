from typing import Literal
import pytest
from chocolatine import SqlType

from src.utils import generate_code, camel_to_snake, cast_to_sql_type


def test_generate_code():
    code = generate_code()
    assert len(code) == 4
    assert code.isdigit()


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("CamelCase", "camel_case"),
        ("ThisIsATest", "this_is_a_test"),
        ("camel2Snake", "camel2_snake"),
        ("getHTTPResponseCode", "get_http_response_code"),
    ],
)
def test_camel_to_snake(
    test_input: (
        Literal["CamelCase"]
        | Literal["ThisIsATest"]
        | Literal["camel2Snake"]
        | Literal["getHTTPResponseCode"]
    ),
    expected: (
        Literal["camel_case"]
        | Literal["this_is_a_test"]
        | Literal["camel2_snake"]
        | Literal["get_http_response_code"]
    ),
):
    assert camel_to_snake(test_input) == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        (str, SqlType.String),
        (int, SqlType.Integer),
        (float, SqlType.Float),
        (bool, SqlType.Boolean),
    ],
)
def test_cast_to_sql_type(
    test_input: type[str] | type[int] | type[float] | type[bool],
    expected: SqlType | SqlType | SqlType | SqlType,
):
    assert cast_to_sql_type(test_input) == expected
