from unittest.mock import MagicMock

from pytest_mock import MockerFixture

from shushu.actions import (
    DataProcessorCoreAction,
    MemoryPayload,
    OpenUrlAction,
    PythonCodeDataProcessorAction,
    SaveDataAction,
    SelectedElementPayload,
    SelectedElementsPayload,
    StorageCoreAction,
    WebAgentCoreAction,
)
from shushu.core import ShushuCore, gen_shushu_core
from shushu.models import BaseDataModel, Element, Url
from shushu.settings import CoreSettings
from shushu.storages.base import BaseStorage
from shushu.storages.factory import StorageFactory
from shushu.web_agents.base import BaseWebAgent
from shushu.web_agents.factory import WebAgentFactory


def test_gen_shushu_core(mocker: MockerFixture, logger_fixture: MagicMock) -> None:
    web_agent = mocker.MagicMock(spec=BaseWebAgent)
    web_agent_factory = mocker.MagicMock(spec=WebAgentFactory)
    web_agent_factory.create.return_value = web_agent
    storage = mocker.MagicMock(spec=BaseStorage)
    storage_factory = mocker.MagicMock(spec=StorageFactory)
    storage_factory.create.return_value = storage
    WebAgentFactoryClass = mocker.patch("shushu.core.WebAgentFactory", return_value=web_agent_factory)
    StorageFactoryClass = mocker.patch("shushu.core.StorageFactory", return_value=storage_factory)
    settings = CoreSettings()
    actual = gen_shushu_core(settings=settings, logger=logger_fixture)
    assert isinstance(actual, ShushuCore)
    assert actual.web_agent == web_agent
    assert actual.logger == logger_fixture
    assert actual.storage == storage
    web_agent_factory.create.assert_called_once_with(settings=settings.web_agent_settings)
    WebAgentFactoryClass.assert_called_once_with(logger=logger_fixture)
    storage_factory.create.assert_called_once_with(settings=settings.storage_settings)
    StorageFactoryClass.assert_called_once_with(logger=logger_fixture)


def test_shushu_core_performs_web_agent_action(mocker: MockerFixture, logger_fixture: MagicMock) -> None:
    web_agent = mocker.MagicMock(spec=BaseWebAgent)
    storage = mocker.MagicMock(spec=BaseStorage)
    sut = ShushuCore(web_agent=web_agent, storage=storage, logger=logger_fixture)
    action = WebAgentCoreAction(action=OpenUrlAction(url=Url(value="http://example.com")))
    with sut:
        sut.perform(action)
        web_agent.perform.assert_called_once_with(action.action)
        web_agent.__enter__.assert_called_once_with()
        web_agent.__exit__.assert_not_called()
    web_agent.__exit__.assert_called_once_with(None, None, None)


def test_shushu_core_performs_storage_action(mocker: MockerFixture, logger_fixture: MagicMock) -> None:
    web_agent = mocker.MagicMock(spec=BaseWebAgent)
    storage = mocker.MagicMock(spec=BaseStorage)
    sut = ShushuCore(web_agent=web_agent, storage=storage, logger=logger_fixture)

    class SomeData(BaseDataModel):
        text: str

    some_data = SomeData(text="http://example.com")
    sut.set_memory(some_data)
    action = StorageCoreAction(payload=MemoryPayload(), action=SaveDataAction(data="data"))
    sut.perform(action)
    storage.perform.assert_called_once_with(action=action.action, payload=some_data)


def test_shushu_core_performs_data_processor_action_memory_payload(
    mocker: MockerFixture, logger_fixture: MagicMock
) -> None:
    web_agent = mocker.MagicMock(spec=BaseWebAgent)
    storage = mocker.MagicMock(spec=BaseStorage)
    DataProcessorFactory = mocker.patch("shushu.core.DataProcessorFactory")
    data_processor_factory = DataProcessorFactory.return_value
    sut = ShushuCore(web_agent=web_agent, storage=storage, logger=logger_fixture)

    class SomeData(BaseDataModel):
        text: str

    some_data = SomeData(text="http://example.com")
    sut.set_memory(some_data)
    action = DataProcessorCoreAction(
        action=PythonCodeDataProcessorAction(
            code="""
from shushu.models import Url, BaseDataModel
class Data(BaseDataModel):
    text: str
def convert(x: Url) -> Data:
    return Data(text=x.value)
"""
        ),
        payload=MemoryPayload(),
    )
    sut.perform(action)

    web_agent.perform.assert_not_called()
    storage.perform.assert_not_called()
    data_processor_factory.create.assert_called_once_with(action=action.action, payload=some_data)
    DataProcessorFactory.assert_called_once_with(logger=logger_fixture)
    assert sut.get_memory() == data_processor_factory.create.return_value.perform.return_value
    data_processor_factory.create.return_value.perform.assert_called_once_with()


def test_shushu_core_performs_data_processor_action_selected_element_payload(
    mocker: MockerFixture, logger_fixture: MagicMock
) -> None:
    web_agent = mocker.MagicMock(spec=BaseWebAgent)
    storage = mocker.MagicMock(spec=BaseStorage)
    DataProcessorFactory = mocker.patch("shushu.core.DataProcessorFactory")
    data_processor_factory = DataProcessorFactory.return_value
    selected_element = Element(url=Url(value="http://example.com"), html_source="<html>aaa</html>")
    web_agent.get_selected_element.return_value = selected_element
    sut = ShushuCore(web_agent=web_agent, storage=storage, logger=logger_fixture)
    action = DataProcessorCoreAction(
        action=PythonCodeDataProcessorAction(
            code="""
from shushu.models import Element, BaseDataModel
class Data(BaseDataModel):
    text: str
def convert(x: Element) -> Data:
    return Data(text=x.text)
"""
        ),
        payload=SelectedElementPayload(),
    )
    sut.perform(action)

    web_agent.perform.assert_not_called()
    storage.perform.assert_not_called()
    data_processor_factory.create.assert_called_once_with(action=action.action, payload=selected_element)
    DataProcessorFactory.assert_called_once_with(logger=logger_fixture)
    assert sut.get_memory() == data_processor_factory.create.return_value.perform.return_value
    data_processor_factory.create.return_value.perform.assert_called_once_with()
    web_agent.get_selected_element.assert_called_once_with()


def test_shushu_core_performs_data_processor_action_selected_elements_payload(
    mocker: MockerFixture, logger_fixture: MagicMock
) -> None:
    web_agent = mocker.MagicMock(spec=BaseWebAgent)
    storage = mocker.MagicMock(spec=BaseStorage)
    DataProcessorFactory = mocker.patch("shushu.core.DataProcessorFactory")
    data_processor_factory = DataProcessorFactory.return_value
    selected_elements = [
        Element(url=Url(value="http://example.com"), html_source="<html>aaa</html>"),
        Element(url=Url(value="http://example.com"), html_source="<html>bbb</html>"),
    ]
    web_agent.get_selected_elements.return_value = selected_elements
    sut = ShushuCore(web_agent=web_agent, storage=storage, logger=logger_fixture)
    action = DataProcessorCoreAction(
        action=PythonCodeDataProcessorAction(
            code="""
from shushu.models import Element, BaseDataModel
class Data(BaseDataModel):
    texts: list[str]
def convert(x: list[Element]) -> Data:
    return Data(texts=[d.text for d in x])
"""
        ),
        payload=SelectedElementsPayload(),
    )
    sut.perform(action)

    web_agent.perform.assert_not_called()
    storage.perform.assert_not_called()
    data_processor_factory.create.assert_called_once_with(action=action.action, payload=selected_elements)
    DataProcessorFactory.assert_called_once_with(logger=logger_fixture)
    assert sut.get_memory() == data_processor_factory.create.return_value.perform.return_value
    data_processor_factory.create.return_value.perform.assert_called_once_with()
    web_agent.get_selected_elements.assert_called_once_with()
