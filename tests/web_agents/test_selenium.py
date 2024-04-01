from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from shushu.models import OpenUrlAction, Url
from shushu.settings import ChromeSeleniumDriverSettings
from shushu.web_agents.exceptions import SeleniumDriverNotReadyError
from shushu.web_agents.selenium import SeleniumWebAgent
from shushu.web_agents.selenium_drivers.base import BaseSeleniumDriver


def test_perform_raises_exception_when_driver_is_not_ready(mocker: MockerFixture, logger_fixture: MagicMock) -> None:
    settings = ChromeSeleniumDriverSettings()

    sut = SeleniumWebAgent(driver_settings=settings, logger=logger_fixture)

    some_action = OpenUrlAction(url=Url(url="http://localhost:8080"))

    with pytest.raises(SeleniumDriverNotReadyError):
        sut.perform(some_action)


def test_perform_calls_driver_perform(mocker: MockerFixture, logger_fixture: MagicMock) -> None:
    settings = ChromeSeleniumDriverSettings()
    selenium_driver = mocker.MagicMock(spec=BaseSeleniumDriver)
    SeleniumDriverFactory = mocker.patch("shushu.web_agents.selenium.SeleniumDriverFactory")
    SeleniumDriverFactory.return_value.create.return_value = selenium_driver
    sut = SeleniumWebAgent(driver_settings=settings, logger=logger_fixture)

    some_action = OpenUrlAction(url=Url(url="http://localhost:8080"))

    with sut:
        sut.perform(some_action)
        assert sut._driver == selenium_driver

    assert sut._driver is None

    SeleniumDriverFactory.assert_called_once_with(logger=logger_fixture)
    SeleniumDriverFactory.return_value.create.assert_called_once_with(settings=settings)
    selenium_driver.perform.assert_called_once_with(action=some_action)
