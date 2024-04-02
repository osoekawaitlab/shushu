from enum import Enum
from typing import Annotated, Literal, Optional, Union

from oltl import BaseEntity, BaseModel, BaseUpdateTimeAwareModel
from pydantic import AnyHttpUrl, Field

from .types import (
    CoreActionId,
    ElementId,
    HtmlSource,
    ImageBinary,
    QueryString,
    SelectorId,
    UrlId,
    UserId,
    UserNameString,
    WebAgentActionId,
    XPath,
)


class Rectangle(BaseModel):
    x: int
    y: int
    width: int
    height: int


class User(BaseUpdateTimeAwareModel, BaseEntity[UserId]):  # type: ignore[misc]
    username: UserNameString


class Url(BaseUpdateTimeAwareModel, BaseEntity[UrlId]):  # type: ignore[misc]
    value: AnyHttpUrl


class CoreActionType(str, Enum):
    WEB_AGENT = "WEB_AGENT"


class WebAgentActionType(str, Enum):
    OPEN_URL = "OPEN_URL"
    SELECT_ELEMENTS = "SELECT_ELEMENTS"
    SELECT_ELEMENT = "SELECT_ELEMENT"


class BaseCoreAction(BaseUpdateTimeAwareModel, BaseEntity[CoreActionId]):  # type: ignore[misc]
    type: CoreActionType


class BaseWebAgentAction(BaseUpdateTimeAwareModel, BaseEntity[WebAgentActionId]):  # type: ignore[misc]
    type: WebAgentActionType


class OpenUrlAction(BaseWebAgentAction):
    type: Literal[WebAgentActionType.OPEN_URL] = WebAgentActionType.OPEN_URL
    url: Url


class SelectorType(str, Enum):
    XPATH = "XPATH"
    RECTANGLE = "RECTANGLE"
    RELATIVE = "RELATIVE"
    MINIMUM_ENCLOSING_ELEMENT_WITH_MULTIPLE_TEXTS = "MINIMUM_ENCLOSING_ELEMENT_WITH_MULTIPLE_TEXTS"


class BaseSelector(BaseUpdateTimeAwareModel, BaseEntity[SelectorId]):  # type: ignore[misc]
    type: SelectorType


class XPathSelector(BaseSelector):
    type: Literal[SelectorType.XPATH] = SelectorType.XPATH
    xpath: XPath


class RectangleSelector(BaseSelector):
    type: Literal[SelectorType.RECTANGLE] = SelectorType.RECTANGLE
    rectangle: Rectangle


class RelativeSelectorType(str, Enum):
    PARENT = "PARENT"
    CHILD = "CHILD"
    SIBLING = "SIBLING"


class RelativeSelector(BaseSelector):
    type: Literal[SelectorType.RELATIVE] = SelectorType.RELATIVE
    relative_type: RelativeSelectorType


class MinimumEnclosingElementWithMultipleTextsSelector(BaseSelector):
    type: Literal[SelectorType.MINIMUM_ENCLOSING_ELEMENT_WITH_MULTIPLE_TEXTS] = (
        SelectorType.MINIMUM_ENCLOSING_ELEMENT_WITH_MULTIPLE_TEXTS
    )
    target_strings: list[QueryString]


Selector = Annotated[Union[XPathSelector, RectangleSelector, RelativeSelector], Field(discriminator="type")]


class SelectElementsAction(BaseWebAgentAction):
    type: Literal[WebAgentActionType.SELECT_ELEMENTS] = WebAgentActionType.SELECT_ELEMENTS
    selector: Selector


class SelectEelementAction(BaseWebAgentAction):
    type: Literal[WebAgentActionType.SELECT_ELEMENT] = WebAgentActionType.SELECT_ELEMENT
    selector: Selector


WebAgentAction = Annotated[
    Union[OpenUrlAction, SelectElementsAction, SelectEelementAction], Field(discriminator="type")
]


class WebAgentCoreAction(BaseCoreAction):
    type: Literal[CoreActionType.WEB_AGENT] = CoreActionType.WEB_AGENT
    action: WebAgentAction


CoreAction = Annotated[WebAgentCoreAction, Field(discriminator="type")]


class Element(BaseUpdateTimeAwareModel, BaseEntity[ElementId]):  # type: ignore[misc]
    url: Url
    html_source: HtmlSource
    screenshot_png: Optional[ImageBinary] = None
    location: Optional[Rectangle] = None


class WebAgentActionResultType(str, Enum):
    NONE = "NONE"
    SINGLE_ELEMENT = "SINGLE_ELEMENT"
    MULTIPLE_ELEMENTS = "MULTIPLE_ELEMENTS"
    ERROR = "ERROR"


class BaseWebAgentActionResult(BaseModel):
    type: WebAgentActionResultType


class NoneWebAgentActionResult(BaseWebAgentActionResult):
    type: Literal[WebAgentActionResultType.NONE] = WebAgentActionResultType.NONE


class SingleElementWebAgentActionResult(BaseWebAgentActionResult):
    type: Literal[WebAgentActionResultType.SINGLE_ELEMENT] = WebAgentActionResultType.SINGLE_ELEMENT
    element: Element


class MultipleElementsWebAgentActionResult(BaseWebAgentActionResult):
    type: Literal[WebAgentActionResultType.MULTIPLE_ELEMENTS] = WebAgentActionResultType.MULTIPLE_ELEMENTS
    elements: list[Element]


class ErrorWebAgentActionResult(BaseWebAgentActionResult):
    type: Literal[WebAgentActionResultType.ERROR] = WebAgentActionResultType.ERROR
    message: str


WebAgentActionResult = Annotated[
    Union[
        NoneWebAgentActionResult,
        SingleElementWebAgentActionResult,
        MultipleElementsWebAgentActionResult,
        ErrorWebAgentActionResult,
    ],
    Field(discriminator="type"),
]
