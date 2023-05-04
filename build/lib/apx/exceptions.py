class ApxException(IOError):
    """
    There was an ambiguous exception
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize WuxException
        """
        super().__init__(*args, **kwargs)

class MissingParam(ApxException):
    """For handling required param is missing"""

class UnSupported(ApxException):
    """For handling unsupported conditional"""

class InvalidValue(ApxException):
    """For handling if some value is invalid"""

class InvalidRequest(ApxException):
    """For handling invalid request"""

class BadReq(ApxException):
    """For handling bad request"""

class SpecificErrResp(ApxException):
    """For spessific error response"""
