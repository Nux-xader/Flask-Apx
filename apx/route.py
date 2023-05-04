import typing as t
from apx.param import Param
from apx.config import ApxConfig
from apx.helpers import capute_err
from flask import current_app as cr_app
from apx.exceptions import (
    BadReq, 
    SpecificErrResp
)


def route(
    param:t.Optional[bool]=True, 
    allowed_role:t.Optional[t.Union[tuple, list]]=tuple()
):
    def decorator(func:t.Callable[[any, any], any]):
        def warper(*args, **kwargs):
            apx:ApxConfig = cr_app.apx
            try:
                if not apx.auth.is_authorized(allowed_role):
                    return {
                        "err": False, 
                        "msg": "Unauthorized", 
                        "data": None
                    }
                if param:
                    resp = func(param=Param(), *args, **kwargs)
                else:
                    resp = func(*args, **kwargs)
                return apx.resp.success(resp)
            except BadReq as e:
                return apx.resp.bad_req(e)
            except SpecificErrResp as e:
                return apx.resp.sepesific_err_resp(e)
            except:
                return {
                    "err": True, 
                    "msg": "server error", 
                    "data": None, 
                    "err_data": capute_err() if cr_app.debug else dict()
                }
        warper.__name__ = func.__name__
        return warper
    return decorator

