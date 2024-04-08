from oltl import BaseModel

from ..base import BaseShushuComponent
from ..models import BaseDataProcessorAction
from .base import BaseDataProcessor


class DataProcessorFactory(BaseShushuComponent):
    def create(self, action: BaseDataProcessorAction, payload: BaseModel) -> BaseDataProcessor:
        raise NotImplementedError()
