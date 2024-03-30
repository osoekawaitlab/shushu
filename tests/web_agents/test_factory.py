from unittest.mock import MagicMock

from pytest_mock import MockerFixture

from shushu.settings import SeleniumWebAgentSettings
from shushu.web_agents.factory import WebAgentFactory


def test_web_agent_factory_creates_selenium_agent(mocker: MockerFixture, logger_fixture: MagicMock) -> None:
    SeleniumWebAgent = mocker.patch("shushu.web_agents.factory.SeleniumWebAgent")
    selenium_web_agent_settings = SeleniumWebAgentSettings()

    actual = WebAgentFactory(logger=logger_fixture).create(settings=selenium_web_agent_settings)

    assert actual == SeleniumWebAgent.return_value
    SeleniumWebAgent.assert_called_once_with(
        driver_settings=selenium_web_agent_settings.driver_settings, logger=logger_fixture
    )
