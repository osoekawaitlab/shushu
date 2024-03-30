from logging import Logger

from ..base import BaseComponentFactory
from ..settings import BaseWebAgentSettings, SeleniumWebAgentSettings
from .base import BaseWebAgent
from .selenium import SeleniumWebAgent


class WebAgentFactory(BaseComponentFactory[BaseWebAgentSettings, BaseWebAgent]):
    def __init__(self, logger: Logger) -> None:
        super(WebAgentFactory, self).__init__(logger=logger)

    def create(self, settings: BaseWebAgentSettings) -> BaseWebAgent:
        if isinstance(settings, SeleniumWebAgentSettings):
            return SeleniumWebAgent(
                driver_settings=settings.driver_settings,
                logger=self.logger,
            )
        raise ValueError(f"Unsupported web agent settings: {settings}")
