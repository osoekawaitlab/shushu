from logging import Logger

from ..models import Url
from .base import BaseWebAgent
from .selenium_drivers.base import BaseSeleniumDriver


class SeleniumWebAgent(BaseWebAgent):
    def __init__(self, driver: BaseSeleniumDriver, target_url: Url, logger: Logger) -> None:
        super(SeleniumWebAgent, self).__init__(target_url=target_url, logger=logger)
        self._driver = driver

    def _start(self) -> None:
        raise NotImplementedError()

    def _end(self) -> None:
        raise NotImplementedError()
