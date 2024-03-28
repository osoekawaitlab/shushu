from unittest.mock import MagicMock

from pytest_mock import MockerFixture

from shushu.settings import ChromeSeleniumDriverSettings
from shushu.web_agents.selenium_drivers.factory import SeleniumDriverFactory


def test_selenium_driver_factory_creates_chrome_driver(mocker: MockerFixture, logger_fixture: MagicMock) -> None:
    ChromeSeleniumDriver = mocker.patch("shushu.web_agents.selenium_drivers.factory.ChromeSeleniumDriver")
    settings = ChromeSeleniumDriverSettings()
    actual = SeleniumDriverFactory(logger=logger_fixture).create(settings=settings)
    assert actual == ChromeSeleniumDriver.return_value
    ChromeSeleniumDriver.assert_called_once_with(logger=logger_fixture)
