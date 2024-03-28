from ..base import BaseComponentFactory
from ..settings import BaseWebAgentSettings, SeleniumWebAgentSettings
from .base import BaseWebAgent
from .selenium import SeleniumWebAgent
from .selenium_drivers.factory import SeleniumDriverFactory


class WebAgentFactory(BaseComponentFactory[BaseWebAgentSettings, BaseWebAgent]):
    def create(self, settings: BaseWebAgentSettings) -> BaseWebAgent:
        if isinstance(settings, SeleniumWebAgentSettings):
            return SeleniumWebAgent(
                logger=self.logger,
                driver=SeleniumDriverFactory(logger=self.logger).create(settings=settings.driver_settings),
            )
        raise ValueError(f"Unsupported web agent settings: {settings}")
