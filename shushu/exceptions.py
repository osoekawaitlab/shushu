class BaseError(Exception):
    def __init__(self, message: str) -> None:
        super(BaseError, self).__init__(message)


class BaseCoreError(BaseError): ...


class MemoryNotSetError(BaseCoreError):
    def __init__(self) -> None:
        super(MemoryNotSetError, self).__init__("Memory is not set.")
