import sys
import traceback
import typing as t
from flask import current_app as cr_app


class ApxResp:
    def __init__(self) -> None:
        self.spesific_err_msgs = tuple()

    def success(self, resp_data):
        if isinstance(resp_data, (type(None), str, bool, float, int, list, dict)):
            return {
                "err": False, 
                "msg": "success", 
                "data": resp_data
            }
        
        return resp_data

    def bad_req(self, e):
        return {
            "err": True, 
            "msg": str(e), 
            "data": None
        }

    def sepesific_err_resp(self, e):
        return {
            "err": True, 
            "msg": parse_err_msg(self.spesific_err_msgs, e) if cr_app.debug else "", 
            "data": None
        }


def try_it(
    #: The function will be call in try statment
    try_func, 
    #: function will be call in except statment, assign dict for spessific exception
    except_funcs:t.Optional[t.Union[t.Callable, dict]]=None,  
    #: the data will be return in except statment
    default=None
):
    try:
        return try_func()
    except Exception as e:
        if except_funcs is not None:
            if isinstance(except_funcs, dict):
                except_func = except_funcs.get(type(e))
                if except_func is None: except_func = except_funcs.get(Exception)
            else:
                except_func = except_funcs

            except_func()
        return default


def capute_err() -> dict:
    ex_type, ex_value, ex_traceback = sys.exc_info()
    return {
        "exception": f"\n{ex_type.__name__}: {ex_value}", 
        "stack":     [
            f"File {trace[0]}, Line {trace[1]}, in {trace[2]}\n{trace[3]}" 
            for trace in traceback.extract_tb(ex_traceback)
        ]
    }


def parse_err_msg(err_list:t.Union[list, tuple], code:str):
    code = str(code).split(":")
    data = tuple()
    if len(code) > 1: data = tuple(code[1:])
    try: return f"{code[0]} >> {err_list[int(code[0])].format(*data)}"
    except: return f"Unknown code: {code}"
