from apx.auth import Auth

class ApxConfig:
    def __init__(self, resp, auth:Auth) -> None:
        self.resp = resp
        self.auth = auth
