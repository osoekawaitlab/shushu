from enum import Enum
from typing import Annotated, Literal, Optional, Union

from bs4 import BeautifulSoup, NavigableString, Tag
from oltl import BaseEntity, BaseModel, BaseUpdateTimeAwareModel
from pydantic import AnyHttpUrl, Field

from .types import (
    ClassSet,
    ClassString,
    CoreActionId,
    ElementId,
    HtmlSource,
    ImageBinary,
    QueryString,
    SelectorId,
    TagString,
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


class Url(BaseModel):
    value: AnyHttpUrl


class CoreActionType(str, Enum):
    WEB_AGENT = "WEB_AGENT"


class WebAgentActionType(str, Enum):
    OPEN_URL = "OPEN_URL"
    SET_SELECTOR = "SET_SELECTOR"
    CLICK_SELECTED_ELEMENT = "CLICK_SELECTED_ELEMENT"


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
    MINIMUM_ENCLOSING_ELEMENT_WITH_MULTIPLE_TEXTS = "MINIMUM_ENCLOSING_ELEMENT_WITH_MULTIPLE_TEXTS"


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


CoreAction = Annotated[WebAgentCoreAction, Field(discriminator="type")]


class Element(BaseUpdateTimeAwareModel, BaseEntity[ElementId]):  # type: ignore[misc]
    url: Url
    html_source: HtmlSource
    screenshot_png: Optional[ImageBinary] = None
    location: Optional[Rectangle] = None

    @property
    def parsed_html(self) -> BeautifulSoup:
        self._parsed_html: BeautifulSoup
        if not hasattr(self, "_parsed_html") or self._parsed_html is None:
            setattr(self, "_parsed_html", BeautifulSoup(self.html_source, "html.parser"))
        return self._parsed_html

    @property
    def root(self) -> Tag | None | NavigableString:
        return self.parsed_html.find(True)

    @property
    def classes(self) -> ClassSet:
        """
        Returns the set of classes of the element.

        Returns:
            ClassSet: The set of classes of the element.

        >>> element = Element(url=Url(value="https://example.com"), html_source="<div class='foo'></div>")
        >>> element.classes
        ClassSet({ClassString('foo')})
        >>> element = Element(url=Url(value="https://example.com"), html_source="<div class='foo bar'></div>")
        >>> element.classes
        ClassSet({ClassString('...'), ClassString('...')})
        >>> element = Element(url=Url(value="https://example.com"), html_source="<div></div>")
        >>> element.classes
        ClassSet()
        """
        if isinstance(self.root, NavigableString) or self.root is None:
            return ClassSet()
        classes = self.root.get("class")
        if classes is None:
            return ClassSet()
        if isinstance(classes, str):
            return ClassSet(ClassString.from_str(c) for c in classes.split(""))
        return ClassSet(ClassString.from_str(c) for c in classes)

    @property
    def tag_name(self) -> TagString | None:
        """
        Returns the tag name of the element.

        Returns:
            str: The tag name of the element.

        >>> element = Element(url=Url(value="https://example.com"), html_source="<div></div>")
        >>> element.tag_name
        TagString('div')
        """
        if isinstance(self.root, NavigableString) or self.root is None:
            return None
        return TagString.from_str(self.root.name)

    @property
    def text(self) -> str:
        """
        Returns the text of the element.

        Returns:
            str: The text of the element.

        >>> element = Element(url=Url(value="https://example.com"), html_source="<div>text</div>")
        >>> element.text
        'text'
        """
        if isinstance(self.root, NavigableString) or self.root is None:
            return ""
        return self.root.get_text()
