from unittest.mock import MagicMock

from pytest_mock import MockerFixture

from shushu.settings import SeleniumWebAgentSettings
from shushu.web_agents.factory import WebAgentFactory


def test_web_agent_factory_creates_selenium_agent(mocker: MockerFixture, logger_fixture: MagicMock) -> None:
    selenium_driver_factory = mocker.patch("shushu.web_agents.factory.SeleniumDriverFactory")
    SeleniumWebAgent = mocker.patch("shushu.web_agents.factory.SeleniumWebAgent")
    selenium_web_agent_settings = SeleniumWebAgentSettings()

    actual = WebAgentFactory(logger=logger_fixture).create(settings=selenium_web_agent_settings)

    assert actual == SeleniumWebAgent.return_value
    selenium_driver_factory.assert_called_once_with(logger=logger_fixture)
    selenium_driver_factory.return_value.create.assert_called_once_with(
        settings=selenium_web_agent_settings.driver_settings
    )
    SeleniumWebAgent.assert_called_once_with(
        driver=selenium_driver_factory.return_value.create.return_value, logger=logger_fixture
    )
