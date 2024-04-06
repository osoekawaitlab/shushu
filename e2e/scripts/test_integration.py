from shushu.logger import get_logger
from shushu.models import (
    MinimumEnclosingElementWithMultipleTextsSelector,
    OpenUrlAction,
    SetSelectorAction,
    Url,
)
from shushu.settings import LoggerSettings, SeleniumWebAgentSettings
from shushu.web_agents.factory import WebAgentFactory


def test_get_minimum_enclosing_element_with_multiple_texts(http_server_fixture: str) -> None:
    logger = get_logger(settings=LoggerSettings())
    settings = SeleniumWebAgentSettings()
    web_agent = WebAgentFactory(logger=logger).create(settings=settings)
    with web_agent:
        web_agent.perform(OpenUrlAction(url=Url(value=http_server_fixture)))
        web_agent.perform(
            SetSelectorAction(selector=MinimumEnclosingElementWithMultipleTextsSelector(target_strings=["始まりの村"]))
        )
        minelem = web_agent.get_selected_element()
        assert minelem.tag_name == "a"
        web_agent.perform(
            SetSelectorAction(
                selector=MinimumEnclosingElementWithMultipleTextsSelector(target_strings=["始まりの村", "2024"])
            )
        )
        minelem = web_agent.get_selected_element()
        assert minelem.tag_name == "li"
        assert "list-item" in minelem.classes
        web_agent.perform(
            SetSelectorAction(
                selector=MinimumEnclosingElementWithMultipleTextsSelector(target_strings=["始まりの村", "装備"])
            )
        )
        minelem = web_agent.get_selected_element()
        assert minelem.tag_name == "ul"
