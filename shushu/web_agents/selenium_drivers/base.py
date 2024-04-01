from collections.abc import Iterable

from ...base import BaseShushuComponent
from ...models import Element, WebAgentAction


class BaseSeleniumDriver(BaseShushuComponent):
    def perform(self, action: WebAgentAction) -> None:
        raise NotImplementedError()

    def get_selected_element(self) -> Element:
        raise NotImplementedError()

    def get_selected_elements(self) -> Iterable[Element]:
        raise NotImplementedError()
