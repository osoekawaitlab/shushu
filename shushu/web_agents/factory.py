from logging import Logger

from ..base import BaseComponentFactory
from ..models import Url
from ..settings import BaseWebAgentSettings, SeleniumWebAgentSettings
from .base import BaseWebAgent
from .selenium import SeleniumWebAgent
from .selenium_drivers.factory import SeleniumDriverFactory


class WebAgentFactory(BaseComponentFactory[BaseWebAgentSettings, BaseWebAgent]):
    def __init__(self, target_url: Url, logger: Logger) -> None:
        super(WebAgentFactory, self).__init__(logger=logger)
        self._target_url = target_url

    def create(self, settings: BaseWebAgentSettings) -> BaseWebAgent:
        if isinstance(settings, SeleniumWebAgentSettings):
            return SeleniumWebAgent(
                logger=self.logger,
                target_url=self._target_url,
                driver=SeleniumDriverFactory(logger=self.logger).create(settings=settings.driver_settings),
            )
        raise ValueError(f"Unsupported web agent settings: {settings}")
