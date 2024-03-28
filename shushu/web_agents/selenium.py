from logging import Logger

from .base import BaseWebAgent
from .selenium_drivers.base import BaseSeleniumDriver


class SeleniumWebAgent(BaseWebAgent):
    def __init__(self, driver: BaseSeleniumDriver, logger: Logger) -> None:
        super(SeleniumWebAgent, self).__init__(logger=logger)
        self._driver = driver
