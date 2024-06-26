from collections.abc import Mapping
from logging import Logger
from typing import Generic, Optional, TypeVar

from .settings import SettingsT

ComponentT = TypeVar("ComponentT", bound="BaseShushuComponent")


class BaseShushuComponent:
    def __init__(self, logger: Logger) -> None:
        self._logger = logger

    @property
    def logger(self) -> Logger:
        return self._logger

    def log_debug(self, message: str, extra: Optional[Mapping[str, object]] = None) -> None:
        self.logger.debug(message, extra=extra if extra is not None else {})

    def log_info(self, message: str, extra: Optional[Mapping[str, object]] = None) -> None:
        self.logger.info(message, extra=extra if extra is not None else {})

    def log_warning(self, message: str, extra: Optional[Mapping[str, object]] = None) -> None:
        self.logger.warning(message, extra=extra if extra is not None else {})

    def log_error(self, message: str, extra: Optional[Mapping[str, object]] = None) -> None:
        self.logger.error(message, extra=extra if extra is not None else {})

    def log_critical(self, message: str, extra: Optional[Mapping[str, object]] = None) -> None:
        self.logger.critical(message, extra=extra if extra is not None else {})


class BaseComponentFactory(BaseShushuComponent, Generic[SettingsT, ComponentT]):
    def __init__(self, logger: Logger) -> None:
        super(BaseComponentFactory, self).__init__(logger=logger)

    def create(self, settings: SettingsT) -> ComponentT:
        raise NotImplementedError
