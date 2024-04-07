import dataclasses
import decimal
import typing as t
import uuid
from datetime import date, datetime

from flask import Flask, Response, jsonify
from flask import typing as ft
from flask.json.provider import DefaultJSONProvider
from werkzeug.http import http_date
from werkzeug.exceptions import default_exceptions, HTTPException


class JinkelaJSONProvider(DefaultJSONProvider):
    def _default(o: t.Any) -> t.Any:
        if isinstance(o, datetime):
            return o.strftime(r"%Y-%m-%d %H:%M:%S")

        if isinstance(o, date):
            return http_date(o)

        if isinstance(o, (decimal.Decimal, uuid.UUID)):
            return str(o)

        if dataclasses and dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)

        if hasattr(o, "__html__"):
            return str(o.__html__())

        raise TypeError(
            f"Object of type {type(o).__name__} is not JSON serializable"
        )  # noqa

    default: t.Callable[[t.Any], t.Any] = staticmethod(_default)


class JinkelaFlask(Flask):
    json_provider_class = JinkelaJSONProvider

    def __init__(self, **kwargs: t.Any):
        super().__init__(**kwargs)  # noqa
        for de in default_exceptions.values():
            self.register_error_handler(de, self._error_handler)

    def _error_handler(self, error: Exception):
        response = jsonify(success=False, message=error.description)
        response.status_code = (
            error.code if isinstance(error, HTTPException) else 500
        )  # noqa
        return response

    def make_response(self, rv: ft.ResponseReturnValue) -> Response:

        if isinstance(rv, (dict, list, tuple)):
            rv = dict(success=True, data=rv)

        return super().make_response(rv)
