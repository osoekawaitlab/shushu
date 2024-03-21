from logging import Logger

from ..base import BaseComponentFactory
from ..core import ShushuCore
from ..settings import InterfaceSettings
from .base import BaseInterface


class InterfaceFactory(BaseComponentFactory[InterfaceSettings, BaseInterface]):
    def __init__(self, core: ShushuCore, logger: Logger) -> None:
        super(InterfaceFactory, self).__init__(logger=logger)
        self._core = core

    def create(self, settings: InterfaceSettings) -> BaseInterface:
        raise NotImplementedError()
