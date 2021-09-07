import typing as t
import functools
from flask import request, jsonify, Response

from pydantic import BaseModel, ValidationError
from sqlalchemy.exc import IntegrityError


class DBConstraintErrorHandler:
    def __init__(
        self,
        db_constraint_name: str,
        field_name: str,
        message: str,
        error_type: str = "integrity_error",
    ):
        self.db_constraint_name = db_constraint_name
        self.field_name = field_name
        self.message = message
        self.error_type = error_type


def _db_error_handler_to_dict(db_error_handler: DBConstraintErrorHandler):
    return {
        "loc": [db_error_handler.field_name],
        "msg": db_error_handler.message,
        "type": f"database.{db_error_handler.error_type}",
    }


def handle_validation_error(error):
    return jsonify({"errors": error.errors()}), 400


def handle_db_error(error, db_constraint_handlers):
    detected_db_constraints = []

    for db_constraint_handler in db_constraint_handlers:
        if db_constraint_handler.db_constraint_name in error.orig.__str__():
            detected_db_constraints.append(db_constraint_handler)

    if len(detected_db_constraints) == 0:
        print(error.orig)
        return Response(status=500)

    errors = [
        _db_error_handler_to_dict(integrity_handler)
        for integrity_handler in detected_db_constraints
    ]
    return jsonify({"errors": errors}), 400


def validate_route(
    schema: t.Type[BaseModel],
    db_constraint_handlers: t.Optional[t.Iterable[DBConstraintErrorHandler]] = None,
) -> t.Callable:
    db_constraint_handlers = (
        tuple() if db_constraint_handlers is None else db_constraint_handlers
    )

    def decorator(func: t.Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if request.method == "POST":
                request_body = request.json or request.form
                if request_body is None:
                    request_body = {}
                instance_fields = {**request_body, **request.view_args}
                try:
                    instance = schema(**instance_fields)
                except ValidationError as error:
                    return handle_validation_error(error)
                try:
                    return func(instance, **request.view_args)
                except IntegrityError as error:
                    return handle_db_error(error, db_constraint_handlers)

        return wrapper

    return decorator
