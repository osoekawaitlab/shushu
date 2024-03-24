from oltl import BaseEntity, BaseUpdateTimeAwareModel

from .types import UserId


class User(BaseEntity[UserId], BaseUpdateTimeAwareModel):
    username: str
