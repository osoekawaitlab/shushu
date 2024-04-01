from ..exceptions import BaseError


class WebAgentError(BaseError):
    pass


class SeleniumDriverNotReadyError(WebAgentError):
    def __init__(self) -> None:
        super(SeleniumDriverNotReadyError, self).__init__("Selenium driver is not ready")
