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


class HtmlSource(TrimmedStringMixIn, NonEmptyStringMixIn): ...


class ImageBinary(BaseBytes): ...


class ClassString(TrimmedStringMixIn, NonEmptyStringMixIn): ...


class ClassSet(set[ClassString]): ...


class TagString(TrimmedStringMixIn, NonEmptyStringMixIn): ...


class DataProcessorId(Id): ...


class DataId(Id): ...


class TypeId(Id): ...


class CodeString(BaseString): ...


class CoreActionType(str, Enum):
    WEB_AGENT = "WEB_AGENT"
    DATA_PROCESSOR = "DATA_PROCESSOR"
    STORAGE = "STORAGE"
    GENERATE_ID = "GENERATE_ID"
    SEQUENCIAL = "SEQUENCIAL"


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


ElementTypeId = TypeId("01HVRW8WGGA24A44DYMG86C5X4")
ElementSequenceTypeId = TypeId("01HVRW90TDQTE16481BCEQ7A88")
IdTypeId = TypeId("01HVA7ZG5GKAK9QVBVV5029H3V")
