from ...base import BaseComponentFactory
from ...settings import BaseSeleniumDriverSettings, ChromeSeleniumDriverSettings
from .base import BaseSeleniumDriver
from .chrome import ChromeSeleniumDriver


class SeleniumDriverFactory(BaseComponentFactory[BaseSeleniumDriverSettings, BaseSeleniumDriver]):
    def create(self, settings: BaseSeleniumDriverSettings) -> BaseSeleniumDriver:
        if isinstance(settings, ChromeSeleniumDriverSettings):
            return ChromeSeleniumDriver(logger=self.logger)
        raise ValueError(f"Unsupported driver settings: {settings}")
