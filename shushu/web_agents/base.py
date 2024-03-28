from logging import Logger

from ..base import BaseShushuComponent


class BaseWebAgent(BaseShushuComponent):
    def __init__(self, logger: Logger):
        super(BaseWebAgent, self).__init__(logger=logger)
