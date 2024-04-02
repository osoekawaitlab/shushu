from selenium.webdriver import Chrome

from .base import BaseSeleniumDriver


class ChromeSeleniumDriver(BaseSeleniumDriver):
    def _init_driver(self) -> None:
        self._driver = Chrome()
