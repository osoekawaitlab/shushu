from ...exceptions import BaseError


class BaseSeleniumDriverError(BaseError):
    pass


class NoElementSelectedError(BaseSeleniumDriverError):
    def __init__(self) -> None:
        super(NoElementSelectedError, self).__init__("No element is selected.")
