from datetime import datetime, timezone
from unittest.mock import MagicMock

from freezegun import freeze_time
from oltl import Id
from pytest_mock import MockerFixture
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from shushu.models import (
    Element,
    MultipleElementsWebAgentActionResult,
    NoneWebAgentActionResult,
    OpenUrlAction,
    SelectEelementAction,
    SelectElementsAction,
    SingleElementWebAgentActionResult,
    Url,
    XPathSelector,
)
from shushu.web_agents.selenium_drivers.base import BaseSeleniumDriver

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


def test_perform_open_url_action(logger_fixture: MagicMock) -> None:
    mock_web_driver.reset_mock()
    sut = DerivedSeleniumDriver(logger=logger_fixture)
    actual = sut.perform(OpenUrlAction(url=Url(value="http://localhost:8080/")))
    mock_web_driver.get.assert_called_once_with(url="http://localhost:8080/")
    assert isinstance(actual, NoneWebAgentActionResult)
    mock_web_driver.reset_mock()


def test_perform_select_element_action(logger_fixture: MagicMock, mocker: MockerFixture) -> None:
    id_ = Id("01HTFESX9K7JAB3K2FQSWPKZKS")
    mocker.patch("oltl.Id.generate", return_value=id_)
    mock_web_driver.reset_mock()
    mock_element = MagicMock(spec=WebElement)
    mock_element.get_attribute.return_value = "<div>test</div>"
    mock_web_driver.find_element.return_value = mock_element
    mock_web_driver.current_url = "http://localhost:8080/"
    dt = datetime(2024, 4, 2, 4, 11, 12, 941018, tzinfo=timezone.utc)
    expected = SingleElementWebAgentActionResult(
        id=id_,
        element=Element(
            id=id_,
            html_source="<div>test</div>",
            url=Url(value="http://localhost:8080/", created_at=dt, updated_at=dt, id=id_),
            created_at=dt,
            updated_at=dt,
        ),
        created_at=dt,
        updated_at=dt,
    )
    sut = DerivedSeleniumDriver(logger=logger_fixture)
    with freeze_time(dt):
        actual = sut.perform(SelectEelementAction(selector=XPathSelector(xpath="//div[@id='test']")))
    assert actual == expected
    mock_web_driver.find_element.assert_called_once_with(By.XPATH, "//div[@id='test']")
    mock_web_driver.reset_mock()


def test_perform_select_element_action_no_such_element(logger_fixture: MagicMock, mocker: MockerFixture) -> None:
    mocker.patch("oltl.Id.generate", return_value=Id("01HTFESX9K7JAB3K2FQSWPKZKS"))
    mock_web_driver.reset_mock()
    mock_web_driver.find_element.return_value = None
    mock_web_driver.find_element.side_effect = NoSuchElementException()
    sut = DerivedSeleniumDriver(logger=logger_fixture)
    actual = sut.perform(SelectEelementAction(selector=XPathSelector(xpath="//div[@id='test']")))
    assert isinstance(actual, NoneWebAgentActionResult)
    mock_web_driver.find_element.assert_called_once_with(By.XPATH, "//div[@id='test']")
    mock_web_driver.reset_mock()


def test_perform_select_element_action_with_last_url(logger_fixture: MagicMock, mocker: MockerFixture) -> None:
    url_id = Id("01HTFKJH9SQ9YNVPW75RF6JS0C")
    id_ = Id("01HTFESX9K7JAB3K2FQSWPKZKS")
    mocker.patch("oltl.Id.generate", return_value=id_)
    mock_web_driver.reset_mock()
    mock_element = MagicMock(spec=WebElement)
    mock_element.get_attribute.return_value = "<div>test</div>"
    mock_web_driver.find_element.side_effect = None
    mock_web_driver.find_element.return_value = mock_element
    mock_web_driver.current_url = "http://localhost:8080/"
    dt = datetime(2024, 4, 2, 4, 11, 12, 941018, tzinfo=timezone.utc)
    url = Url(value="http://localhost:8080/", id=url_id)
    expected = SingleElementWebAgentActionResult(
        id=id_,
        element=Element(
            id=id_,
            html_source="<div>test</div>",
            url=url,
            created_at=dt,
            updated_at=dt,
        ),
        created_at=dt,
        updated_at=dt,
    )
    sut = DerivedSeleniumDriver(logger=logger_fixture)
    sut.perform(OpenUrlAction(url=url))
    with freeze_time(dt):
        actual = sut.perform(SelectEelementAction(selector=XPathSelector(xpath="//div[@id='test']")))
    assert actual == expected
    mock_web_driver.find_element.assert_called_once_with(By.XPATH, "//div[@id='test']")
    mock_web_driver.reset_mock()


def test_perform_select_elements_action(logger_fixture: MagicMock, mocker: MockerFixture) -> None:
    id_ = Id("01HTFM98TZWX0A52DMGQARK516")
    mocker.patch("oltl.Id.generate", return_value=id_)
    mock_web_driver.reset_mock()
    mock_elements = [MagicMock(spec=WebElement), MagicMock(spec=WebElement)]
    mock_elements[0].get_attribute.return_value = "<div>test0</div>"
    mock_elements[1].get_attribute.return_value = "<div>test1</div>"
    mock_web_driver.find_elements.return_value = mock_elements
    mock_web_driver.current_url = "http://localhost:8080/"
    dt = datetime(2024, 4, 2, 5, 44, 41, 434553, tzinfo=timezone.utc)
    expected = MultipleElementsWebAgentActionResult(
        id=id_,
        elements=[
            Element(
                id=id_,
                html_source="<div>test0</div>",
                url=Url(value="http://localhost:8080/", created_at=dt, updated_at=dt, id=id_),
                created_at=dt,
                updated_at=dt,
            ),
            Element(
                id=id_,
                html_source="<div>test1</div>",
                url=Url(value="http://localhost:8080/", created_at=dt, updated_at=dt, id=id_),
                created_at=dt,
                updated_at=dt,
            ),
        ],
        created_at=dt,
        updated_at=dt,
    )
    sut = DerivedSeleniumDriver(logger=logger_fixture)
    with freeze_time(dt):
        actual = sut.perform(SelectElementsAction(selector=XPathSelector(xpath="//div[@id='test']")))
    assert actual == expected
    mock_web_driver.find_elements.assert_called_once_with(By.XPATH, "//div[@id='test']")
    mock_web_driver.reset_mock()


def test_perform_select_elements_action_no_such_element(logger_fixture: MagicMock, mocker: MockerFixture) -> None:
    mocker.patch("oltl.Id.generate", return_value=Id("01HTFM98TZWX0A52DMGQARK516"))
    mock_web_driver.reset_mock()
    mock_web_driver.find_elements.return_value = []
    mock_web_driver.find_elements.side_effect = NoSuchElementException()
    sut = DerivedSeleniumDriver(logger=logger_fixture)
    actual = sut.perform(SelectElementsAction(selector=XPathSelector(xpath="//div[@id='test']")))
    assert isinstance(actual, NoneWebAgentActionResult)
    mock_web_driver.find_elements.assert_called_once_with(By.XPATH, "//div[@id='test']")
    mock_web_driver.reset_mock()


def test_perform_select_elements_action_with_last_url(logger_fixture: MagicMock, mocker: MockerFixture) -> None:
    url_id = Id("01HTFKJH9SQ9YNVPW75RF6JS0C")
    id_ = Id("01HTFM98TZWX0A52DMGQARK516")
    mocker.patch("oltl.Id.generate", return_value=id_)
    mock_web_driver.reset_mock()
    mock_elements = [MagicMock(spec=WebElement), MagicMock(spec=WebElement)]
    mock_elements[0].get_attribute.return_value = "<div>test0</div>"
    mock_elements[1].get_attribute.return_value = "<div>test1</div>"
    mock_web_driver.find_elements.side_effect = None
    mock_web_driver.find_elements.return_value = mock_elements
    mock_web_driver.current_url = "http://localhost:8080/"
    dt = datetime(2024, 4, 2, 5, 44, 41, 434553, tzinfo=timezone.utc)
    url = Url(value="http://localhost:8080/", id=url_id)
    expected = MultipleElementsWebAgentActionResult(
        id=id_,
        elements=[
            Element(
                id=id_,
                html_source="<div>test0</div>",
                url=url,
                created_at=dt,
                updated_at=dt,
            ),
            Element(
                id=id_,
                html_source="<div>test1</div>",
                url=url,
                created_at=dt,
                updated_at=dt,
            ),
        ],
        created_at=dt,
        updated_at=dt,
    )
    sut = DerivedSeleniumDriver(logger=logger_fixture)
    sut.perform(OpenUrlAction(url=url))
    with freeze_time(dt):
        actual = sut.perform(SelectElementsAction(selector=XPathSelector(xpath="//div[@id='test']")))
    assert actual == expected
    mock_web_driver.find_elements.assert_called_once_with(By.XPATH, "//div[@id='test']")
    mock_web_driver.reset_mock()
