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
from ...types import QueryString
from .exceptions import NoElementSelectedError


class BaseSeleniumDriver(BaseShushuComponent):
    def __init__(self, logger: Logger) -> None:
        super(BaseSeleniumDriver, self).__init__(logger=logger)
        self._init_driver()
        self._driver: WebDriver
        self._selected_element: Element | list[Element] | None = None

    def __del__(self) -> None:
        self._driver.quit()

    @abstractmethod
    def _init_driver(self) -> None:
        raise NotImplementedError()

    def _find_minimum_enclosing_element_with_multiple_texts(
        self, element: WebElement, target_strings: list[QueryString]
    ) -> WebElement | None:
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
            return NoneWebAgentActionResult()
        if isinstance(action, SelectElementAction):
            try:
                if isinstance(action.selector, XPathSelector):
                    element = self._driver.find_element(By.XPATH, action.selector.xpath)
                elif isinstance(action.selector, MinimumEnclosingElementWithMultipleTextsSelector):
                    tmp = self._find_minimum_enclosing_element_with_multiple_texts(
                        self._driver.find_element(By.XPATH, "/*"), action.selector.target_strings
                    )
                    if tmp is None:
                        raise NoSuchElementException()
                    element = tmp
            except NoSuchElementException:
                return NoneWebAgentActionResult()
            url = Url(value=self._driver.current_url)
            self._selected_element = Element(url=url, html_source=element.get_attribute("outerHTML"))
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
            url = Url(value=self._driver.current_url)
            self._selected_element = [Element(url=url, html_source=d.get_attribute("outerHTML")) for d in elements]
            return MultipleElementsWebAgentActionResult(elements=self._selected_element.copy())
        RectangleSelector,
        raise NotImplementedError()

    def get_selected_element(self) -> Element:
        if self._selected_element is None:
            raise NoElementSelectedError()
        if isinstance(self._selected_element, list):
            return self._selected_element[0]
        return self._selected_element

    def get_selected_elements(self) -> list[Element]:
        if self._selected_element is None:
            raise NoElementSelectedError()
        if isinstance(self._selected_element, Element):
            return [self._selected_element]
        return self._selected_element
