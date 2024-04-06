from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest
from freezegun import freeze_time
from oltl import Id
from pytest_mock import MockerFixture
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from shushu.models import (
    ClickSelectedElementAction,
    Element,
    OpenUrlAction,
    SetSelectorAction,
    Url,
    XPathSelector,
)
from shushu.web_agents.selenium_drivers.base import BaseSeleniumDriver
from shushu.web_agents.selenium_drivers.exceptions import (
    NoElementFoundError,
    NoElementSelectedError,
)

mock_web_driver = MagicMock(spec=WebDriver)


class DerivedSeleniumDriver(BaseSeleniumDriver):
    def _init_driver(self) -> None:
        self._driver = mock_web_driver


def test_constructor_and_destructor(logger_fixture: MagicMock) -> None:
    mock_web_driver.reset_mock()

    sut = DerivedSeleniumDriver(logger=logger_fixture)
    assert sut._driver == mock_web_driver
    del sut
    mock_web_driver.quit.assert_called_once_with()
    mock_web_driver.reset_mock()


def test_get_selected_element_raises_error_when_no_element_is_selected(logger_fixture: MagicMock) -> None:
    sut = DerivedSeleniumDriver(logger=logger_fixture)
    with pytest.raises(NoElementSelectedError):
        sut.get_selected_element()


def test_get_selected_elements_raises_error_when_no_element_is_selected(logger_fixture: MagicMock) -> None:
    sut = DerivedSeleniumDriver(logger=logger_fixture)
    with pytest.raises(NoElementSelectedError):
        sut.get_selected_elements()


def test_perform_open_url_action(logger_fixture: MagicMock) -> None:
    mock_web_driver.reset_mock()
    sut = DerivedSeleniumDriver(logger=logger_fixture)
    sut.perform(OpenUrlAction(url=Url(value="http://localhost:8080/")))
    mock_web_driver.get.assert_called_once_with(url="http://localhost:8080/")
    mock_web_driver.reset_mock()


def test_perform_set_selector_and_get(logger_fixture: MagicMock, mocker: MockerFixture) -> None:
    id_ = Id("01HTFESX9K7JAB3K2FQSWPKZKS")
    mocker.patch("oltl.Id.generate", return_value=id_)
    mock_web_driver.reset_mock()

    dt = datetime(2024, 4, 2, 4, 11, 12, 941018, tzinfo=timezone.utc)

    mock_web_driver.reset_mock()
    mock_elements = [MagicMock(spec=WebElement), MagicMock(spec=WebElement)]
    mock_elements[0].get_attribute.return_value = "<div>test0</div>"
    mock_elements[1].get_attribute.return_value = "<div>test1</div>"
    mock_web_driver.find_element.return_value = mock_elements[0]
    mock_web_driver.find_elements.return_value = mock_elements
    mock_web_driver.find_element.side_effect = None
    mock_web_driver.find_elements.side_effect = None
    mock_web_driver.current_url = "http://localhost:8080/"
    sut = DerivedSeleniumDriver(logger=logger_fixture)
    sut.perform(SetSelectorAction(selector=XPathSelector(xpath="//div[@id='test']")))
    expected_selected_element = Element(
        id=id_, url=Url(value="http://localhost:8080/"), html_source="<div>test0</div>", created_at=dt, updated_at=dt
    )
    with freeze_time(dt):
        actual_selected_element = sut.get_selected_element()
    assert actual_selected_element == expected_selected_element
    expected_selected_elements = [
        Element(
            id=id_,
            url=Url(value="http://localhost:8080/"),
            html_source="<div>test0</div>",
            created_at=dt,
            updated_at=dt,
        ),
        Element(
            id=id_,
            url=Url(value="http://localhost:8080/"),
            html_source="<div>test1</div>",
            created_at=dt,
            updated_at=dt,
        ),
    ]
    with freeze_time(dt):
        actual_selected_elements = sut.get_selected_elements()
    assert actual_selected_elements == expected_selected_elements
    mock_web_driver.find_element.assert_called_once_with(By.XPATH, "//div[@id='test']")
    mock_web_driver.find_elements.assert_called_once_with(By.XPATH, "//div[@id='test']")
    mock_web_driver.reset_mock()


def test_perform_select_element_action_no_element_found_error(logger_fixture: MagicMock, mocker: MockerFixture) -> None:
    mocker.patch("oltl.Id.generate", return_value=Id("01HTFESX9K7JAB3K2FQSWPKZKS"))
    mock_web_driver.reset_mock()
    mock_web_driver.find_element.return_value = None
    mock_web_driver.find_element.side_effect = NoSuchElementException()
    sut = DerivedSeleniumDriver(logger=logger_fixture)
    sut.perform(SetSelectorAction(selector=XPathSelector(xpath="//div[@id='test']")))
    with pytest.raises(NoElementFoundError):
        sut.get_selected_element()
    mock_web_driver.find_element.assert_called_once_with(By.XPATH, "//div[@id='test']")
    mock_web_driver.reset_mock()


def test_perform_click_selected_element_raises_error_when_no_element_is_selected(logger_fixture: MagicMock) -> None:
    sut = DerivedSeleniumDriver(logger=logger_fixture)
    with pytest.raises(NoElementSelectedError):
        sut.perform(action=ClickSelectedElementAction())


def test_perform_click_selected_element_raises_error_when_no_element_found(
    logger_fixture: MagicMock, mocker: MockerFixture
) -> None:
    mock_web_driver.reset_mock()
    mock_web_driver.find_element.return_value = None
    mock_web_driver.find_element.side_effect = NoSuchElementException()
    sut = DerivedSeleniumDriver(logger=logger_fixture)
    sut.perform(SetSelectorAction(selector=XPathSelector(xpath="//div[@id='test']")))
    with pytest.raises(NoElementFoundError):
        sut.perform(action=ClickSelectedElementAction())
    mock_web_driver.find_element.assert_called_once_with(By.XPATH, "//div[@id='test']")
    mock_web_driver.reset_mock()


def test_perform_click_selected_element_success(logger_fixture: MagicMock, mocker: MockerFixture) -> None:
    mocker.patch("oltl.Id.generate", return_value=Id("01HTFESX9K7JAB3K2FQSWPKZKS"))
    mock_web_driver.reset_mock()
    mock_web_driver.find_element.return_value = MagicMock(spec=WebElement)
    mock_web_driver.find_element.side_effect = None
    sut = DerivedSeleniumDriver(logger=logger_fixture)
    sut.perform(SetSelectorAction(selector=XPathSelector(xpath="//div[@id='test']")))
    sut.perform(action=ClickSelectedElementAction())
    mock_web_driver.find_element.assert_called_once_with(By.XPATH, "//div[@id='test']")
    mock_web_driver.find_element.return_value.click.assert_called_once_with()
    mock_web_driver.reset_mock()
