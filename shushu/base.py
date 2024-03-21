from logging import Logger
from typing import Generic, TypeVar

from .settings import SettingsT

ComponentT = TypeVar("ComponentT", bound="BaseShushuComponent")


class BaseShushuComponent:
    def __init__(self, logger: Logger) -> None:
        self._logger = logger

    @property
    def logger(self) -> Logger:
        return self._logger


class BaseComponentFactory(BaseShushuComponent, Generic[SettingsT, ComponentT]):
    def __init__(self, logger: Logger) -> None:
        super(BaseComponentFactory, self).__init__(logger=logger)

    def create(self, settings: SettingsT) -> ComponentT:
        raise NotImplementedError
