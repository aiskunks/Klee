import typing as t
import functools
from flask import request, jsonify, Response, make_response, session
from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import BaseQuery

from pydantic import BaseModel, ValidationError
from klee_engine.models.exceptions import DatabaseException


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


def _validate_create(create_func, schema, fields, db_handlers, **create_kwargs):
    try:
        validated_fields = schema(**fields)
    except ValidationError as error:
        return handle_validation_error(error)
    try:
        return create_func(**{**validated_fields.dict(), **create_kwargs})
    except (IntegrityError, DatabaseException) as error:
        return handle_db_error(error, db_handlers)


def validate_post(
        schema_in: t.Type[BaseModel],
        db_handlers: t.Optional[t.Iterable[DBConstraintErrorHandler]] = None,
) -> t.Callable:
    db_handlers = (
        tuple() if db_handlers is None else db_handlers
    )

    def decorator(func: t.Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if request.method == "POST":
                request_body = request.json or request.form
                if request_body is None:
                    request_body = {}
                instance_fields = {**request_body, **request.view_args}

                return _validate_create(
                    create_func=func,
                    schema=schema_in,
                    fields=instance_fields,
                    db_handlers=db_handlers,
                    **request.view_args,
                )

        return wrapper

    return decorator


def serialize_response(schema_out: t.Type[BaseModel]) -> t.Callable:
    def decorator(func: t.Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            instance_or_query = func(*args, **kwargs)
            return schema_out.from_orm(instance_or_query).dict()

        return wrapper

    return decorator


def serialize_response_list(schema_out: t.Type[BaseModel], list_kwarg=None) -> t.Callable:
    def decorator(func: t.Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            query = func(*args, **kwargs)
            return schema_out(**{list_kwarg: list(query)}).dict()

        return wrapper

    return decorator


def allow_cookie_from_cors(func: t.Callable):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        response_str = func(*args, **kwargs)
        response = make_response(response_str)
        response.set_cookie('same-site-cookie', 'session', samesite='Lax')
        # Ensure you use "add" to not overwrite existing cookie headers
        response.headers.add('Set-Cookie', 'cross-site-cookie=session; SameSite=None; Secure')
        print("IAMFUCKING HERE")
        print(request.headers.get("Set-Cookie"))
        print(session)
        return response

    return wrapper
