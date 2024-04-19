from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from shushu.data_processors.python_code import PythonCodeDataProcessor
from shushu.models import BaseDataModel, Element, ElementSequence, Url
from shushu.types import CodeString, TypeId


def test_python_code_data_processor_perform_element_to_data(mocker: MockerFixture, logger_fixture: MagicMock) -> None:
    payload = Element(url=Url(value="http://localhost:8000"), html_source="<div>test</div>")
    src = CodeString(
        """\
from shushu.models import BaseDataModel, Element
from shushu.types import TypeId

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


def test_python_code_data_processor_perform_element_sequence_to_data(
    mocker: MockerFixture, logger_fixture: MagicMock
) -> None:
    payload = ElementSequence(
        elements=[
            Element(url=Url(value="http://localhost:8000"), html_source="<div>test1</div>"),
            Element(url=Url(value="http://localhost:8000"), html_source="<div>test2</div>"),
        ]
    )
    src = CodeString(
        """\
from shushu.models import BaseDataModel, ElementSequence
from shushu.types import TypeId

class DataModel(BaseDataModel):
    type_id: TypeId = TypeId("01HVVGH8C2CYRBJ2KVWXJFTS7H")
    value: str

def convert(element_sequence: ElementSequence) -> DataModel:
    return DataModel(value=chr(10).join(element.text for element in element_sequence.elements))
"""
    )
    sut = PythonCodeDataProcessor(code=src, payload=payload, logger=logger_fixture)
    actual = sut.perform()
    assert hasattr(actual, "value")
    assert actual.value == "test1\ntest2"
    assert actual.type_id == "01HVVGH8C2CYRBJ2KVWXJFTS7H"


def test_python_code_data_processor_perform_raises_type_error_when_payload_is_not_supported(
    mocker: MockerFixture, logger_fixture: MagicMock
) -> None:
    class DataModel(BaseDataModel):
        type_id: TypeId = TypeId("01HVVGR5KPZSARHDQE6X4MVCP5")

    payload = DataModel()
    src = CodeString(
        """\
from shushu.models import BaseDataModel
from shushu.types import TypeId

class DataModel(BaseDataModel):
    type_id: TypeId = TypeId("01HVVGR5KPZSARHDQE6X4MVCP5")

def convert(data: DataModel) -> DataModel:
    return data
"""
    )
    sut = PythonCodeDataProcessor(code=src, payload=payload, logger=logger_fixture)
    with pytest.raises(TypeError):
        sut.perform()
