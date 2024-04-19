from ..actions import BaseDataProcessorAction, PythonCodeDataProcessorAction
from ..base import BaseShushuComponent
from ..models import BaseDataModel
from .base import BaseDataProcessor
from .python_code import PythonCodeDataProcessor


class DataProcessorFactory(BaseShushuComponent):
    def create(self, action: BaseDataProcessorAction, payload: BaseDataModel) -> BaseDataProcessor:
        if isinstance(action, PythonCodeDataProcessorAction):
            return PythonCodeDataProcessor(
                code=action.code,
                payload=payload,
                logger=self.logger,
            )
        raise NotImplementedError()
