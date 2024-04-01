class BaseError(Exception):
    def __init__(self, message: str) -> None:
        super(BaseError, self).__init__(message)
