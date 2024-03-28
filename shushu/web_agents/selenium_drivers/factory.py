from ...base import BaseComponentFactory
from ...settings import BaseSeleniumDriverSettings
from .base import BaseSeleniumDriver


class SeleniumDriverFactory(BaseComponentFactory[BaseSeleniumDriverSettings, BaseSeleniumDriver]):
    def create(self, settings: BaseSeleniumDriverSettings) -> BaseSeleniumDriver:
        raise NotImplementedError()
