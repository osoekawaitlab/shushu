from typing import Annotated, Literal, Optional, Union

from oltl import BaseEntity, BaseModel, BaseUpdateTimeAwareModel
from pydantic import Field

from .models import Rectangle, Url
from .types import (
    CodeString,
    CoreActionId,
    CoreActionType,
    DataProcessorId,
    DataProcessorType,
    PayloadType,
    QueryString,
    SelectorId,
    SelectorType,
    StorageActionType,
    WebAgentActionId,
    WebAgentActionType,
    XPath,
)


class BaseCoreAction(BaseUpdateTimeAwareModel, BaseEntity[CoreActionId]):  # type: ignore[misc]
    type: CoreActionType


class BaseWebAgentAction(BaseUpdateTimeAwareModel, BaseEntity[WebAgentActionId]):  # type: ignore[misc]
    type: WebAgentActionType


class OpenUrlAction(BaseWebAgentAction):
    type: Literal[WebAgentActionType.OPEN_URL] = WebAgentActionType.OPEN_URL
    url: Url


class BaseSelector(BaseUpdateTimeAwareModel, BaseEntity[SelectorId]):  # type: ignore[misc]
    type: SelectorType


class XPathSelector(BaseSelector):
    type: Literal[SelectorType.XPATH] = SelectorType.XPATH
    xpath: XPath


class RectangleSelector(BaseSelector):
    type: Literal[SelectorType.RECTANGLE] = SelectorType.RECTANGLE
    rectangle: Rectangle


class MinimumEnclosingElementWithMultipleTextsSelector(BaseSelector):
    type: Literal[SelectorType.MINIMUM_ENCLOSING_ELEMENT_WITH_MULTIPLE_TEXTS] = (
        SelectorType.MINIMUM_ENCLOSING_ELEMENT_WITH_MULTIPLE_TEXTS
    )
    target_strings: list[QueryString]


Selector = Annotated[
    Union[XPathSelector, RectangleSelector, MinimumEnclosingElementWithMultipleTextsSelector],
    Field(discriminator="type"),
]


class SetSelectorAction(BaseWebAgentAction):
    type: Literal[WebAgentActionType.SET_SELECTOR] = WebAgentActionType.SET_SELECTOR
    selector: Selector


class ClickSelectedElementAction(BaseWebAgentAction):
    type: Literal[WebAgentActionType.CLICK_SELECTED_ELEMENT] = WebAgentActionType.CLICK_SELECTED_ELEMENT


WebAgentAction = Annotated[
    Union[OpenUrlAction, SetSelectorAction, ClickSelectedElementAction], Field(discriminator="type")
]


class WebAgentCoreAction(BaseCoreAction):
    type: Literal[CoreActionType.WEB_AGENT] = CoreActionType.WEB_AGENT
    action: WebAgentAction


class BasePayload(BaseModel):
    type: PayloadType


class MemoryPayload(BasePayload):
    type: Literal[PayloadType.MEMORY] = PayloadType.MEMORY


class SelectedElementPayload(BasePayload):
    type: Literal[PayloadType.SELECTED_ELEMENT] = PayloadType.SELECTED_ELEMENT


class SelectedElementsPayload(BasePayload):
    type: Literal[PayloadType.SELECTED_ELEMENTS] = PayloadType.SELECTED_ELEMENTS


Payload = Annotated[Union[MemoryPayload, SelectedElementPayload, SelectedElementsPayload], Field(discriminator="type")]


class BaseDataProcessorAction(BaseUpdateTimeAwareModel, BaseEntity[DataProcessorId]):  # type: ignore[misc]
    type: DataProcessorType


class PythonCodeDataProcessorAction(BaseDataProcessorAction):
    type: Literal[DataProcessorType.PYTHON_CODE] = DataProcessorType.PYTHON_CODE
    code: CodeString


DataProcessor = Annotated[PythonCodeDataProcessorAction, Field(discriminator="type")]


class DataProcessorCoreAction(BaseCoreAction):
    type: Literal[CoreActionType.DATA_PROCESSOR] = CoreActionType.DATA_PROCESSOR
    action: DataProcessor
    payload: Payload


class BaseStorageAction(BaseUpdateTimeAwareModel, BaseEntity[CoreActionId]):  # type: ignore[misc]
    type: StorageActionType


class SaveDataAction(BaseStorageAction):
    type: Literal[StorageActionType.SAVE_DATA] = StorageActionType.SAVE_DATA


StorageAction = Annotated[SaveDataAction, Field(discriminator="type")]


class StorageCoreAction(BaseCoreAction):
    type: Literal[CoreActionType.STORAGE] = CoreActionType.STORAGE
    action: StorageAction
    payload: Optional[Payload] = None


CoreAction = Annotated[
    Union[WebAgentCoreAction, DataProcessorCoreAction, StorageCoreAction], Field(discriminator="type")
]
