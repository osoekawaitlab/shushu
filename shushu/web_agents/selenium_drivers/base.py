from abc import abstractmethod
from logging import Logger

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from ...actions import (
    ClickSelectedElementAction,
    MinimumEnclosingElementWithMultipleTextsSelector,
    OpenUrlAction,
    RectangleSelector,
    Selector,
    SetSelectorAction,
    WebAgentAction,
    XPathSelector,
)
from ...base import BaseShushuComponent
from ...models import Element, Url
from ...types import QueryString
from .exceptions import NoElementFoundError, NoElementSelectedError


class BaseSeleniumDriver(BaseShushuComponent):
    def __init__(self, logger: Logger) -> None:
        super(BaseSeleniumDriver, self).__init__(logger=logger)
        self._init_driver()
        self._driver: WebDriver
        self._selector: Selector | None = None

    def __del__(self) -> None:
        self._driver.quit()

    @abstractmethod
    def _init_driver(self) -> None:
        raise NotImplementedError()

    @property
    def selector(self) -> Selector:
        if self._selector is None:
            raise NoElementSelectedError()
        return self._selector

    def _find_minimum_enclosing_element_with_multiple_texts(
        self, element: WebElement, target_strings: list[QueryString]
    ) -> WebElement:
        text = element.text
        if any(target_string not in text for target_string in target_strings):
            raise NoSuchElementException()
        try:
            for child in element.find_elements(By.XPATH, "*"):
                try:
                    result = self._find_minimum_enclosing_element_with_multiple_texts(child, target_strings)
                except NoSuchElementException:
                    result = None
                if result is not None:
                    return result
        except NoSuchElementException:
            ...
        return element

    def perform(self, action: WebAgentAction) -> None:
        if isinstance(action, OpenUrlAction):
            self._driver.get(url=str(action.url.value))
            return
        if isinstance(action, SetSelectorAction):
            self._selector = action.selector
            return
        if isinstance(action, ClickSelectedElementAction):
            raw_element = self._get_raw_selected_element()
            if raw_element is None:
                raise NoElementFoundError()
            raw_element.click()
            return
        RectangleSelector,
        raise NotImplementedError()

    def _get_raw_selected_element(self) -> WebElement:
        try:
            if isinstance(self.selector, XPathSelector):
                return self._driver.find_element(By.XPATH, self.selector.xpath)
            elif isinstance(self.selector, MinimumEnclosingElementWithMultipleTextsSelector):
                return self._find_minimum_enclosing_element_with_multiple_texts(
                    self._driver.find_element(By.XPATH, "/*"), self.selector.target_strings
                )
            else:
                raise NotImplementedError()
        except NoSuchElementException:
            raise NoElementFoundError()

    def get_selected_element(self) -> Element:
        element = self._get_raw_selected_element()
        return Element(
            url=Url(value=self._driver.current_url),
            html_source=element.get_attribute("outerHTML"),
        )

    def get_selected_elements(self) -> list[Element]:
        if self._selector is None:
            raise NoElementSelectedError()
        try:
            if isinstance(self._selector, XPathSelector):
                elements = self._driver.find_elements(By.XPATH, self._selector.xpath)
            else:
                raise NotImplementedError()
        except NoSuchElementException:
            raise NoElementFoundError()
        url = Url(value=self._driver.current_url)
        return [Element(url=url, html_source=d.get_attribute("outerHTML")) for d in elements]
