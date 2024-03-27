from logging import Logger

from ..base import BaseComponentFactory
from ..core import ShushuCore
from ..settings import CliInterfaceSettings, InterfaceSettings
from .base import BaseInterface
from .cli import CliInterface


class InterfaceFactory(BaseComponentFactory[InterfaceSettings, BaseInterface]):
    def __init__(self, core: ShushuCore, logger: Logger) -> None:
        super(InterfaceFactory, self).__init__(logger=logger)
        self._core = core

    def create(self, settings: InterfaceSettings) -> BaseInterface:
        if isinstance(settings, CliInterfaceSettings):
            return CliInterface(core=self._core, logger=self._logger)
        raise TypeError(f"Unsupported settings type: {type(settings)}")
