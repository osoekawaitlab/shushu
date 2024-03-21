from logging import Logger

from ..base import BaseShushuComponent
from ..core import ShushuCore


class BaseInterface(BaseShushuComponent):
    def __init__(self, core: ShushuCore, logger: Logger) -> None:
        super(BaseInterface, self).__init__(logger=logger)
        self._core = core

    @property
    def core(self) -> ShushuCore:
        return self._core

    def run(self, target: str) -> None:
        raise NotImplementedError
