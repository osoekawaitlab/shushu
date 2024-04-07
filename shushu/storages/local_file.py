from logging import Logger

from ..settings import NewOrExistingPath
from .base import BaseStorage


class LocalFileStorage(BaseStorage):
    def __init__(self, path: NewOrExistingPath, logger: Logger):
        super(LocalFileStorage, self).__init__(logger=logger)
        self._path = path
        if not self._path.exists():
            self._path.mkdir(parents=True)
