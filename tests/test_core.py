from unittest.mock import MagicMock

from pytest_mock import MockerFixture

from shushu.core import ShushuCore, gen_shushu_core
from shushu.models import OpenUrlAction, Url, WebAgentCoreAction
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


def test_shushu_core_performs_web_agent_action(mocker: MockerFixture, logger_fixture: MagicMock) -> None:
    web_agent = mocker.MagicMock(spec=BaseWebAgent)
    sut = ShushuCore(web_agent=web_agent, logger=logger_fixture)
    action = WebAgentCoreAction(action=OpenUrlAction(url=Url(value="http://example.com")))
    with sut:
        sut.perform(action)
        web_agent.perform.assert_called_once_with(action.action)
        web_agent.__enter__.assert_called_once_with()
        web_agent.__exit__.assert_not_called()
    web_agent.__exit__.assert_called_once_with(None, None, None)
