import typing as t


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



