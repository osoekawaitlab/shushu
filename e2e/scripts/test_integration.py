from shushu.logger import get_logger
from shushu.models import (
    MinimumEnclosingElementWithMultipleTextsSelector,
    OpenUrlAction,
    SelectElementAction,
    Url,
)
from shushu.settings import LoggerSettings
from shushu.web_agents.selenium_drivers.chrome import ChromeSeleniumDriver


def test_get_minimum_enclosing_element_with_multiple_texts(http_server_fixture: str) -> None:
    logger = get_logger(settings=LoggerSettings())
    driver = ChromeSeleniumDriver(logger=logger)
    driver.perform(OpenUrlAction(url=Url(value=http_server_fixture)))
    driver.perform(
        SelectElementAction(selector=MinimumEnclosingElementWithMultipleTextsSelector(target_strings=["始まりの村"]))
    )
    minelem = driver.get_selected_element()
    assert minelem.tag_name == "a"
    driver.perform(
        SelectElementAction(
            selector=MinimumEnclosingElementWithMultipleTextsSelector(target_strings=["始まりの村", "2024"])
        )
    )
    minelem = driver.get_selected_element()
    assert minelem.tag_name == "li"
    assert "list-item" in minelem.classes
    driver.perform(
        SelectElementAction(
            selector=MinimumEnclosingElementWithMultipleTextsSelector(target_strings=["始まりの村", "装備"])
        )
    )
    minelem = driver.get_selected_element()
    assert minelem.tag_name == "ul"
