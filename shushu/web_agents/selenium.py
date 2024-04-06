from collections.abc import Sequence
from logging import Logger

from ..models import Element, WebAgentAction
from ..settings import SeleniumDriverSettings
from .base import BaseWebAgent
from .exceptions import SeleniumDriverNotReadyError
from .selenium_drivers.base import BaseSeleniumDriver
from .selenium_drivers.factory import SeleniumDriverFactory


class SeleniumWebAgent(BaseWebAgent):
    def __init__(self, driver_settings: SeleniumDriverSettings, logger: Logger) -> None:
        super(SeleniumWebAgent, self).__init__(logger=logger)
        self._driver_settings = driver_settings
        self._driver: BaseSeleniumDriver | None = None

    @property
    def driver(self) -> BaseSeleniumDriver:
        if self._driver is None:
            raise SeleniumDriverNotReadyError()
        return self._driver

    def _start(self) -> None:
        self._driver = SeleniumDriverFactory(logger=self._logger).create(settings=self._driver_settings)

    def _end(self) -> None:
        del self._driver
        self._driver = None

    def perform(self, action: WebAgentAction) -> None:
        return self.driver.perform(action=action)

    def get_selected_element(self) -> Element:
        return self.driver.get_selected_element()

    def get_selected_elements(self) -> Sequence[Element]:
        return self.driver.get_selected_elements()
