from ..base import BaseShushuComponent
from ..models import BaseDataModel


class BaseDataProcessor(BaseShushuComponent):
    def perform(self) -> BaseDataModel:
        raise NotImplementedError()
