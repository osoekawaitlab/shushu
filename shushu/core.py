from contextlib import AbstractContextManager
from logging import Logger
from types import TracebackType

from .base import BaseShushuComponent
from .models import CoreAction, WebAgentCoreAction
from .settings import CoreSettings
from .web_agents.base import BaseWebAgent
from .web_agents.factory import WebAgentFactory


class ShushuCore(BaseShushuComponent, AbstractContextManager["ShushuCore"]):
    def __init__(self, logger: Logger, web_agent: BaseWebAgent) -> None:
        super(ShushuCore, self).__init__(logger=logger)
        self._web_agent = web_agent

    @property
    def web_agent(self) -> BaseWebAgent:
        return self._web_agent

    def __enter__(self) -> "ShushuCore":
        self.web_agent.__enter__()
        return self

    def __exit__(
        self,
        __exc_type: type[BaseException] | None,
        __exc_value: BaseException | None,
        __traceback: TracebackType | None,
    ) -> bool | None:
        self.web_agent.__exit__(__exc_type, __exc_value, __traceback)
        return None

    def perform(self, action: CoreAction) -> None:
        print(f"Performing action: {action}")
        if isinstance(action, WebAgentCoreAction):
            self.web_agent.perform(action.action)
            return
        raise NotImplementedError()


def gen_shushu_core(settings: CoreSettings, logger: Logger) -> ShushuCore:
    web_agent_factory = WebAgentFactory(logger=logger)
    web_agent = web_agent_factory.create(settings=settings.web_agent_settings)
    return ShushuCore(logger=logger, web_agent=web_agent)
