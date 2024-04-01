from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from shushu.models import OpenUrlAction, Url
from shushu.settings import ChromeSeleniumDriverSettings
from shushu.web_agents.exceptions import SeleniumDriverNotReadyError
from shushu.web_agents.selenium import SeleniumWebAgent


def test_perform_raises_exception_when_driver_is_not_ready(mocker: MockerFixture, logger_fixture: MagicMock) -> None:
    settings = ChromeSeleniumDriverSettings()

    sut = SeleniumWebAgent(driver_settings=settings, logger=logger_fixture)

    some_action = OpenUrlAction(url=Url(url="http://localhost:8080"))

    with pytest.raises(SeleniumDriverNotReadyError):
        sut.perform(some_action)
