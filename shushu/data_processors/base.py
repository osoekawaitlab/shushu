from logging import Logger

from ..base import BaseShushuComponent
from ..models import BaseDataModel


class BaseDataProcessor(BaseShushuComponent):
    def __init__(self, payload: BaseDataModel, logger: Logger):
        super(BaseDataProcessor, self).__init__(logger=logger)
        self._payload = payload

    @property
    def payload(self) -> BaseDataModel:
        return self._payload

    def perform(self) -> BaseDataModel:
        raise NotImplementedError()
