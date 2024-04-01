from ...base import BaseShushuComponent
from ...models import WebAgentAction


class BaseSeleniumDriver(BaseShushuComponent):
    def perform(self, action: WebAgentAction) -> None:
        raise NotImplementedError()
