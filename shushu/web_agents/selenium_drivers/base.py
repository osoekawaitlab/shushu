from abc import abstractmethod
from logging import Logger

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from ...base import BaseShushuComponent
from ...models import (
    Element,
    MinimumEnclosingElementWithMultipleTextsSelector,
    MultipleElementsWebAgentActionResult,
    NoneWebAgentActionResult,
    OpenUrlAction,
    RectangleSelector,
    SelectElementAction,
    SelectElementsAction,
    SingleElementWebAgentActionResult,
    Url,
    WebAgentAction,
    WebAgentActionResult,
    XPathSelector,
)


class BaseSeleniumDriver(BaseShushuComponent):
    def __init__(self, logger: Logger) -> None:
        super(BaseSeleniumDriver, self).__init__(logger=logger)
        self._init_driver()
        self._driver: WebDriver
        self._last_url: Url | None = None

    def __del__(self) -> None:
        self._driver.quit()

    @abstractmethod
    def _init_driver(self) -> None:
        raise NotImplementedError()

    def _find_minimum_enclosing_element_with_multiple_texts(
        self, element: WebElement, target_strings: list[str]
    ) -> WebElement:
        text = element.text
        if any(target_string not in text for target_string in target_strings):
            return None
        try:
            for child in element.find_elements(By.XPATH, "*"):
                result = self._find_minimum_enclosing_element_with_multiple_texts(child, target_strings)
                if result is not None:
                    return result
        except NoSuchElementException:
            ...
        return element

    def perform(self, action: WebAgentAction) -> WebAgentActionResult:
        if isinstance(action, OpenUrlAction):
            self._driver.get(url=str(action.url.value))
            self._last_url = action.url
            return NoneWebAgentActionResult()
        if isinstance(action, SelectElementAction):
            try:
                if isinstance(action.selector, XPathSelector):
                    element = self._driver.find_element(By.XPATH, action.selector.xpath)
                elif isinstance(action.selector, MinimumEnclosingElementWithMultipleTextsSelector):
                    element = self._find_minimum_enclosing_element_with_multiple_texts(
                        self._driver.find_element(By.XPATH, "/"), action.selector.target_strings
                    )
            except NoSuchElementException:
                return NoneWebAgentActionResult()
            if self._last_url is not None and str(self._last_url.value) == self._driver.current_url:
                url = self._last_url
            else:
                url = Url(value=self._driver.current_url)
            return SingleElementWebAgentActionResult(
                element=Element(url=url, html_source=element.get_attribute("outerHTML"))
            )
        if isinstance(action, SelectElementsAction):
            try:
                if isinstance(action.selector, XPathSelector):
                    elements = self._driver.find_elements(By.XPATH, action.selector.xpath)
                else:
                    raise NotImplementedError()
            except NoSuchElementException:
                return NoneWebAgentActionResult()
            if self._last_url is not None and str(self._last_url.value) == self._driver.current_url:
                url = self._last_url
            else:
                url = Url(value=self._driver.current_url)
            return MultipleElementsWebAgentActionResult(
                elements=[Element(url=url, html_source=d.get_attribute("outerHTML")) for d in elements]
            )
        MinimumEnclosingElementWithMultipleTextsSelector,
        RectangleSelector,
        raise NotImplementedError()
