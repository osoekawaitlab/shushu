from ..exceptions import BaseError


class BaseDataProcessorError(BaseError):
    pass


class PythonCodeError(BaseDataProcessorError):
    def __init__(self, message: str):
        super(PythonCodeError, self).__init__(message)
