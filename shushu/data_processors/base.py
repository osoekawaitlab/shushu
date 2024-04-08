from oltl import BaseModel

from ..base import BaseShushuComponent


class BaseDataProcessor(BaseShushuComponent):
    def perform(self) -> BaseModel:
        raise NotImplementedError()
