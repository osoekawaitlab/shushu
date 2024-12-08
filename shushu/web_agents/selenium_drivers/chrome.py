from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from .base import BaseSeleniumDriver


class ChromeSeleniumDriver(BaseSeleniumDriver):
    def _init_driver(self) -> None:
        options = Options()
        options.add_argument("--disable-gpu")
        options.add_argument("--headless")

        self._driver = Chrome(options=options)
