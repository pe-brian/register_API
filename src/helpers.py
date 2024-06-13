from functools import wraps
from typing import Any

from flask import jsonify, request


def field(field_name: str, field_type: Any, required: bool = True):
    """Decorator to get a field value on request and make it required enventually and inject it"""

    def field_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if required:
                value = request.json.get(field_name)
                if not value:
                    return jsonify({f"message": f"{field_name} is required"}), 400
                if not isinstance(value, field_type):
                    return (
                        jsonify(
                            {f"message": f"{field_name} has not the type expected"}
                        ),
                        400,
                    )
            kwargs[field_name] = value
            return func(*args, **kwargs)

        return wrapper

    return field_decorator
