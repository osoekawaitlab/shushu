from ..base import BaseComponentFactory
from ..settings import BaseStorageSettings
from .base import BaseStorage
from .local_file import LocalFileStorage


class StorageFactory(BaseComponentFactory[BaseStorageSettings, BaseStorage]):
    def create(self, settings: BaseStorageSettings) -> BaseStorage:
        if settings.type == settings.type.LOCAL_FILE:
            return LocalFileStorage(path=settings.path, logger=self._logger)
        raise ValueError(f"Unsupported storage type: {settings.type}")
