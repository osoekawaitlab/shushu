from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from logging import Logger
from types import TracebackType
from typing import Optional, Type, TypeVar

from ..base import BaseShushuComponent

WebAgentT = TypeVar("WebAgentT", bound="BaseWebAgent")


class BaseWebAgent(BaseShushuComponent, AbstractContextManager["BaseWebAgent"], ABC):
    def __init__(self, logger: Logger):
        super(BaseWebAgent, self).__init__(logger=logger)

    @abstractmethod
    def _start(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _end(self) -> None:
        raise NotImplementedError()

    def __enter__(self: WebAgentT) -> WebAgentT:
        self._start()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self._end()
