from logging import Logger

from .base import BaseShushuComponent
from .models import CoreAction
from .settings import CoreSettings
from .web_agents.base import BaseWebAgent
from .web_agents.factory import WebAgentFactory


class ShushuCore(BaseShushuComponent):
    def __init__(self, logger: Logger, web_agent: BaseWebAgent) -> None:
        super(ShushuCore, self).__init__(logger=logger)
        self._web_agent = web_agent

    @property
    def web_agent(self) -> BaseWebAgent:
        return self._web_agent

    def perform(self, action: CoreAction) -> None:
        raise NotImplementedError()


def gen_shushu_core(settings: CoreSettings, logger: Logger) -> ShushuCore:
    web_agent_factory = WebAgentFactory(logger=logger)
    web_agent = web_agent_factory.create(settings=settings.web_agent_settings)
    return ShushuCore(logger=logger, web_agent=web_agent)
