from typing import Optional

from oltl import BaseModel

from ..base import BaseShushuComponent
from ..models import StorageAction


class BaseStorage(BaseShushuComponent):
    def perform(self, action: StorageAction, payload: Optional[BaseModel] = None) -> None: ...
