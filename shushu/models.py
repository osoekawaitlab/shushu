from collections.abc import Sequence
from typing import Any, Optional

from bs4 import BeautifulSoup, NavigableString, Tag
from oltl import BaseEntity, BaseModel, BaseUpdateTimeAwareModel, json_schema_to_model
from pydantic import AnyHttpUrl

from .types import (
    ClassSet,
    ClassString,
    DataId,
    ElementSequenceTypeId,
    ElementTypeId,
    HtmlSource,
    ImageBinary,
    TagString,
    TypeId,
    UserId,
    UserNameString,
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


class BaseDataModel(BaseUpdateTimeAwareModel, BaseEntity[DataId]):  # type: ignore[misc]
    type_id: TypeId


class Element(BaseDataModel):
    type_id: TypeId = ElementTypeId
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


class ElementSequence(BaseDataModel):
    type_id: TypeId = ElementSequenceTypeId
    elements: Sequence[Element]


def json_schema_to_data_model(json_schema: dict[str, Any]) -> type[BaseDataModel]:
    """Create a Pydantic model from a JSON schema.

    Args:
        json_schema (dict): The JSON schema.

    Returns:
        type[BaseDataModel]: The Pydantic model.

    >>> from freezegun import freeze_time
    >>> from unittest.mock import patch
    >>> from oltl import Id, Timestamp
    >>> class ADataModel(BaseDataModel):
    ...     type_id: TypeId = TypeId("01HVA7ZG5GKAK9QVBVV5029H3V")
    ...     a: int
    ...     b: str
    ...
    >>> expected = ADataModel(id=DataId('01HV9913KVW7R5G0XFKDD3JM21'), created_at=Timestamp(1712962126123456), updated_at=Timestamp(1712962126123456), a=1, b="2")
    >>> json_schema = ADataModel.model_json_schema()
    >>> dynamic_model = json_schema_to_data_model(json_schema)
    >>> dynamic_model(id="01HV9913KVW7R5G0XFKDD3JM21", created_at=1712962126123456, updated_at=1712962126123456, type_id="01HVA7ZG5GKAK9QVBVV5029H3V", a=1, b="2")
    ADataModel(id='01HV9913KVW7R5G0XFKDD3JM21', created_at=1712962126123456, updated_at=1712962126123456, type_id='01HVA7ZG5GKAK9QVBVV5029H3V', a=1, b='2')
    """  # noqa: E501
    dynamic_model = json_schema_to_model(json_schema, BaseDataModel)
    if not issubclass(dynamic_model, BaseDataModel):
        raise ValueError(f"Expected a subclass of BaseDataModel, but got {dynamic_model}")
    return dynamic_model
