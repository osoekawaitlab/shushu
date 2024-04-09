from typing import Optional

from ..actions import StorageAction
from ..base import BaseShushuComponent
from ..models import ArgumentType


class BaseStorage(BaseShushuComponent):
    def perform(self, action: StorageAction, payload: Optional[ArgumentType] = None) -> None: ...
