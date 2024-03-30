from unittest.mock import MagicMock

from pytest_mock import MockerFixture

from shushu.core import ShushuCore, gen_shushu_core
from shushu.settings import CoreSettings
from shushu.web_agents.base import BaseWebAgent
from shushu.web_agents.factory import WebAgentFactory


def test_gen_shushu_core(mocker: MockerFixture, logger_fixture: MagicMock) -> None:
    web_agent = mocker.MagicMock(spec=BaseWebAgent)
    web_agent_factory = mocker.MagicMock(spec=WebAgentFactory)
    web_agent_factory.create.return_value = web_agent
    WebAgentFactoryClass = mocker.patch("shushu.core.WebAgentFactory", return_value=web_agent_factory)
    settings = CoreSettings()
    actual = gen_shushu_core(settings=settings, logger=logger_fixture)
    assert isinstance(actual, ShushuCore)
    assert actual.web_agent == web_agent
    assert actual.logger == logger_fixture
    web_agent_factory.create.assert_called_once_with(settings=settings.web_agent_settings)
    WebAgentFactoryClass.assert_called_once_with(logger=logger_fixture)
