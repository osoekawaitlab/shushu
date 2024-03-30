from oltl import BaseEntity, BaseUpdateTimeAwareModel
from pydantic import AnyHttpUrl

from .types import UrlId, UserId, UserNameString


class User(BaseUpdateTimeAwareModel, BaseEntity[UserId]):  # type: ignore[misc]
    username: UserNameString


class Url(BaseUpdateTimeAwareModel, BaseEntity[UrlId]):  # type: ignore[misc]
    url: AnyHttpUrl
