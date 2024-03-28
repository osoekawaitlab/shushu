from logging import Logger

from .base import BaseSeleniumDriver


class ChromeSeleniumDriver(BaseSeleniumDriver):
    def __init__(self, logger: Logger):
        super(ChromeSeleniumDriver, self).__init__(logger=logger)
