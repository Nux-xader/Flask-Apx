import typing as t
from flask import request
from apx.helpers import try_it
from apx.exceptions import (
    BadReq, UnSupported, InvalidValue
)


class Param:
    '''
    Parse param value on GET and POST method
    '''
    def __init__(self) -> None:
        self.params = dict()
        self.json = False
        self.content_type = None

    def missing_param(self, name:str):
        raise BadReq(f"param {name} is require")

    def invalid_param_value(self, name:str, msg:str):
        raise BadReq(f"param {name} must be {msg}")

    def dump(self, method:str):
        if method == "GET":
            self.params = dict(request.args).copy()
        elif method == "POST":
            if self.content_type is None:
                content_type = request.headers.get('Content-Type') or request.headers.get('content-type')
                content_type = str(content_type).lower()
                self.content_type = content_type

            if "application/json" in self.content_type:
                self.json = True
                self.params = request.json
            else:
                self.params = dict(request.form)
        else:
            raise UnSupported(f"Unsupported request method {method}")

    def text(
        self, 
        #: param name default None for getting full json data
        name:t.Optional[str]=None, 
        expected_type=...,  
        is_require:bool=False, 
        default_val=None
    ):
        """
        getting param value by param name in request GET or POST method
        """
        if default_val is not None and is_require:
            raise InvalidValue("default value can't set if is_require=True")

        if self.params == dict(): self.dump(request.method)

        data = default_val
        if name is not None:
            data = try_it(
                try_func=lambda: self.params[name], 
                except_funcs=lambda: self.missing_param(name=name) if is_require else None, 
                default=default_val
            )

        if not isinstance(expected_type, type(Ellipsis)):
            if not isinstance(data, expected_type):
                self.invalid_param_value(name, f'{expected_type.__name__} not {type(data).__name__}')

        return data

