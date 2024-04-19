from unittest.mock import MagicMock

from pytest_mock import MockerFixture

from shushu.data_processors.python_code import PythonCodeDataProcessor
from shushu.models import Element, Url
from shushu.types import CodeString


def test_python_code_data_processor_performance(mocker: MockerFixture, logger_fixture: MagicMock) -> None:
    payload = Element(url=Url(value="http://localhost:8000"), html_source="<div>test</div>")
    src = CodeString(
        """\
from shushu.models import BaseDataModel, TypeId, Element

class DataModel(BaseDataModel):
    type_id: TypeId = TypeId("01HVVFMAGJ8898QE22XAMT9ZQ8")
    value: str

def convert(element: Element) -> DataModel:
    return DataModel(value=element.text)
"""
    )
    sut = PythonCodeDataProcessor(code=src, payload=payload, logger=logger_fixture)
    actual = sut.perform()
    assert hasattr(actual, "value")
    assert actual.value == "test"
    assert actual.type_id == "01HVVFMAGJ8898QE22XAMT9ZQ8"
