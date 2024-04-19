from unittest.mock import MagicMock

from pytest_mock import MockerFixture

from shushu.actions import PythonCodeDataProcessorAction
from shushu.data_processors.factory import DataProcessorFactory
from shushu.models import Element, Url


def test_factory_create_python_code_data_processor(mocker: MockerFixture, logger_fixture: MagicMock) -> None:
    PythonCodeDataProcessor = mocker.patch("shushu.data_processors.factory.PythonCodeDataProcessor")
    payload = Element(url=Url(value="http://localhost:8000"), html_source="<div>test</div>")
    src = """\
def convert(element: Element) -> Element:
    return element
"""
    action = PythonCodeDataProcessorAction(
        code=src,
        payload=payload,
    )
    sut = DataProcessorFactory(logger=logger_fixture)
    actual = sut.create(action=action, payload=payload)
    assert PythonCodeDataProcessor.return_value == actual
    PythonCodeDataProcessor.assert_called_once_with(code=src, payload=payload, logger=logger_fixture)
