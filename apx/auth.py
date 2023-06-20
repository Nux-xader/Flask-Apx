import jwt
import typing as t
from flask import request


class Auth:
    def __init__(self, secret_key:str, list_role:t.Union[list, tuple], get_role_info:t.Callable) -> None:
        self.__secret_key = secret_key
        self.list_role = list_role
        self.get_role_info = get_role_info
    
    def create(self, data:dict) -> str:
        return jwt.encode(data, self.__secret_key, algorithm='HS256')

    def get(self) -> dict:
        token = request.headers.get('apx-access-token')
        print(token)
        if (token is None) or (not token): return dict()
        try: return jwt.decode(token, self.__secret_key, algorithms=['HS256'])
        except: return dict()

    def is_authorized(self, allowed_role:t.Union[list, tuple]) -> bool:
        if len(allowed_role) == 0: return True
        return self.get_role_info(self.get()) in allowed_role
