from logging import Logger

from .base import BaseSeleniumDriver


class ChromeDriver(BaseSeleniumDriver):
    def __init__(self, loggger: Logger):
        super(ChromeDriver, self).__init__(logger=loggger)
