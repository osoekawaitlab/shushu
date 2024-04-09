from ..actions import BaseDataProcessorAction
from ..base import BaseShushuComponent
from ..models import ArgumentType
from .base import BaseDataProcessor


class DataProcessorFactory(BaseShushuComponent):
    def create(self, action: BaseDataProcessorAction, payload: ArgumentType) -> BaseDataProcessor:
        raise NotImplementedError()
