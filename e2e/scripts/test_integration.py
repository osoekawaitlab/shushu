from shushu.core import gen_shushu_core
from shushu.logger import get_logger
from shushu.models import (
    MinimumEnclosingElementWithMultipleTextsSelector,
    OpenUrlAction,
    SetSelectorAction,
    Url,
    WebAgentCoreAction,
    XPathSelector,
)
from shushu.settings import CoreSettings, LoggerSettings


def test_get_minimum_enclosing_element_with_multiple_texts(http_server_fixture: str) -> None:
    settings = CoreSettings()
    logger = get_logger(settings=LoggerSettings())
    core = gen_shushu_core(settings=settings, logger=logger)
    with core:
        core.perform(action=WebAgentCoreAction(action=OpenUrlAction(url=Url(value=http_server_fixture))))
        core.perform(
            action=WebAgentCoreAction(
                action=SetSelectorAction(
                    selector=MinimumEnclosingElementWithMultipleTextsSelector(target_strings=["始まりの村", "2024"])
                )
            )
        )
        minelem = core.web_agent.get_selected_element()
        assert minelem.tag_name == "li"
        assert "list-item" in minelem.classes
        core.perform(
            action=WebAgentCoreAction(
                action=SetSelectorAction(selector=XPathSelector(xpath="//li[contains(@class, 'list-item')]"))
            )
        )
        similar_elems = core.web_agent.get_selected_elements()
        assert len(similar_elems) == 3
        for elem in similar_elems:
            assert elem.tag_name == "li"
            assert "list-item" in elem.classes
