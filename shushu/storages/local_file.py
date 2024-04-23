from logging import Logger

from shushu.actions import SaveDataAction, StorageAction
from shushu.models import BaseDataModel

from ..settings import NewOrExistingPath
from .base import BaseStorage


class LocalFileStorage(BaseStorage):
    def __init__(self, path: NewOrExistingPath, logger: Logger):
        super(LocalFileStorage, self).__init__(logger=logger)
        self._path = path
        if not self._path.exists():
            self._path.mkdir(parents=True)

    def perform(self, action: StorageAction, payload: BaseDataModel | None = None) -> None:
        if isinstance(action, SaveDataAction):
            return self._save_data(payload)
        raise NotImplementedError()

    def _save_data(self, data: BaseDataModel | None) -> None:
        if data is None:
            raise ValueError("No data to save")
        type_id = data.type_id
        dir_to_save = self._path / str(type_id)
        if not dir_to_save.exists():
            dir_to_save.mkdir()
        with open(dir_to_save / f"{data.id}.json", "w", encoding="utf-8") as f:
            f.write(data.model_dump_json())
