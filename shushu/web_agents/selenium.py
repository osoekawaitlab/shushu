from collections.abc import Iterable
from logging import Logger

from ..models import Element, WebAgentAction
from ..settings import SeleniumDriverSettings
from .base import BaseWebAgent


class SeleniumWebAgent(BaseWebAgent):
    def __init__(self, driver_settings: SeleniumDriverSettings, logger: Logger) -> None:
        super(SeleniumWebAgent, self).__init__(logger=logger)
        self._driver_settings = driver_settings

    def _start(self) -> None:
        raise NotImplementedError()

    def _end(self) -> None:
        raise NotImplementedError()

    def perform(self, action: WebAgentAction) -> None:
        raise NotImplementedError()

    def get_selected_element(self) -> Element:
        raise NotImplementedError()

    def get_selected_elements(self) -> Iterable[Element]:
        raise NotImplementedError()
