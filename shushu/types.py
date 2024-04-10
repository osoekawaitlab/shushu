from enum import Enum

from oltl import BaseBytes, BaseString, Id, NonEmptyStringMixIn, TrimmedStringMixIn


class UserId(Id): ...


class UserNameString(NonEmptyStringMixIn, TrimmedStringMixIn): ...


class SessionId(Id): ...


class SelectorId(Id): ...


class CoreActionId(Id): ...


class WebAgentActionId(Id): ...


class XPath(TrimmedStringMixIn, NonEmptyStringMixIn): ...


class QueryString(TrimmedStringMixIn, NonEmptyStringMixIn): ...


class ElementId(Id): ...


class HtmlSource(TrimmedStringMixIn, NonEmptyStringMixIn): ...


class ImageBinary(BaseBytes): ...


class ClassString(TrimmedStringMixIn, NonEmptyStringMixIn): ...


class ClassSet(set[ClassString]): ...


class TagString(TrimmedStringMixIn, NonEmptyStringMixIn): ...


class DataProcessorId(Id): ...


class DataId(Id): ...


class CodeString(BaseString): ...


class CoreActionType(str, Enum):
    WEB_AGENT = "WEB_AGENT"
    DATA_PROCESSOR = "DATA_PROCESSOR"
    STORAGE = "STORAGE"


class WebAgentActionType(str, Enum):
    OPEN_URL = "OPEN_URL"
    SET_SELECTOR = "SET_SELECTOR"
    CLICK_SELECTED_ELEMENT = "CLICK_SELECTED_ELEMENT"


class SelectorType(str, Enum):
    XPATH = "XPATH"
    RECTANGLE = "RECTANGLE"
    MINIMUM_ENCLOSING_ELEMENT_WITH_MULTIPLE_TEXTS = "MINIMUM_ENCLOSING_ELEMENT_WITH_MULTIPLE_TEXTS"


class PayloadType(str, Enum):
    MEMORY = "MEMORY"
    SELECTED_ELEMENT = "SELECTED_ELEMENT"
    SELECTED_ELEMENTS = "SELECTED_ELEMENTS"


class StorageActionType(str, Enum):
    SAVE_DATA = "SAVE_DATA"


class DataProcessorType(str, Enum):
    PYTHON_CODE = "PYTHON_CODE"
