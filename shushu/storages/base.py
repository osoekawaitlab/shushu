from typing import Optional

from ..actions import StorageAction
from ..base import BaseShushuComponent
from ..models import BaseDataModel


class BaseStorage(BaseShushuComponent):
    def perform(self, action: StorageAction, payload: Optional[BaseDataModel] = None) -> None: ...
