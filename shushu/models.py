from collections.abc import Sequence
from typing import Any, Optional, Union

from bs4 import BeautifulSoup, NavigableString, Tag
from oltl import BaseEntity, BaseModel, BaseUpdateTimeAwareModel
from pydantic import AnyHttpUrl, create_model
from pydantic.alias_generators import to_snake

from .types import (
    ClassSet,
    ClassString,
    DataId,
    ElementId,
    HtmlSource,
    ImageBinary,
    TagString,
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


class BaseDataModel(BaseUpdateTimeAwareModel, BaseEntity[DataId]):  # type: ignore[misc]
    pass


ArgumentType = Union[Element, Sequence[Element], BaseDataModel]


def json_schema_to_data_model(json_schema: dict[str, Any]) -> type[BaseDataModel]:
    """Create a Pydantic model from a JSON schema.

    Args:
        json_schema (dict): The JSON schema.

    Returns:
        type[BaseDataModel]: The Pydantic model.

    >>> from freezegun import freeze_time
    >>> from unittest.mock import patch
    >>> from oltl import Id
    >>> from datetime import datetime, timezone
    >>> class ADataModel(BaseDataModel):
    ...     a: int
    ...     b: str
    ...
    >>> expected = ADataModel(a=1, b="2")
    >>> json_schema = ADataModel.model_json_schema()
    >>> dynamic_model = json_schema_to_data_model(json_schema)
    >>> ts = datetime(2024, 4, 12, 22, 48, 46, 123456, timezone.utc)
    >>> with patch("oltl.Id.generate", return_value=Id("01HV9913KVW7R5G0XFKDD3JM21")), freeze_time(ts):
    ...     dynamic_model(a=1, b="2")
    ADataModel(id=DataId('01HV9913KVW7R5G0XFKDD3JM21'), created_at=Timestamp(1712962126123456), updated_at=Timestamp(1712962126123456), a=1, b='2')
    """  # noqa: E501
    class_name = json_schema["title"] if isinstance(json_schema["title"], str) else "DynamicDataModel"
    dynamic_model = create_model(
        class_name,
        __base__=BaseDataModel,
        **{
            to_snake(k): ({"integer": int, "string": str, "number": float, "boolean": bool}.get(v["type"], str), ...)
            for k, v in json_schema["properties"].items()
            if to_snake(k) not in BaseDataModel.model_fields
        },
    )  # type: ignore[call-overload]
    if not isinstance(dynamic_model, type):
        raise TypeError("The dynamic model is not a type.")
    return dynamic_model
