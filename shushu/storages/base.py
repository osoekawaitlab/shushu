from typing import Optional

from oltl import BaseModel

from ..actions import StorageAction
from ..base import BaseShushuComponent


class BaseStorage(BaseShushuComponent):
    def perform(self, action: StorageAction, payload: Optional[BaseModel] = None) -> None: ...
