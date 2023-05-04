import typing as t
from flask import session


class Auth:
    def __init__(self, list_role:t.Union[list, tuple], get_role_info:t.Callable) -> None:
        self.list_role = list_role
        self.get_role_info = get_role_info

    def update(self, data) -> None:
        session.update(data)

    def delete(self, keys:t.Union[list, tuple]) -> None:
        tuple(session.pop(key, None) for key in keys)

    def get(self) -> dict:
        return dict(session)

    def is_authorized(self, allowed_role:t.Union[list, tuple]) -> bool:
        if len(allowed_role) == 0: return True
        return self.get_role_info(self.get()) in allowed_role
