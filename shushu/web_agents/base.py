from contextlib import AbstractContextManager
from logging import Logger
from types import TracebackType
from typing import Optional, Type, TypeVar

from ..base import BaseShushuComponent
from ..models import Url


class BaseWebAgent(BaseShushuComponent):
    def __init__(self, logger: Logger):
        super(BaseWebAgent, self).__init__(logger=logger)

    def open(self, url: Url) -> None:
        raise NotImplementedError()

    def quit(self) -> None:
        raise NotImplementedError()


WebAgentT = TypeVar("WebAgentT", bound=BaseWebAgent)


class WebAgentContext(AbstractContextManager[WebAgentT]):
    def __init__(self, web_agent: WebAgentT, url: Url):
        self._web_agent = web_agent
        self._url = url

    @property
    def web_agent(self) -> WebAgentT:
        return self._web_agent

    @property
    def url(self) -> Url:
        return self._url

    def __enter__(self) -> WebAgentT:
        self.web_agent.open(url=self.url)
        return self.web_agent

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        self.web_agent.quit()
        return None
