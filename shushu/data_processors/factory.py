from oltl import BaseModel

from ..actions import BaseDataProcessorAction
from ..base import BaseShushuComponent
from .base import BaseDataProcessor


class DataProcessorFactory(BaseShushuComponent):
    def create(self, action: BaseDataProcessorAction, payload: BaseModel) -> BaseDataProcessor:
        raise NotImplementedError()
