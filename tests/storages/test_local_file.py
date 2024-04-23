import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock

from shushu.actions import SaveDataAction
from shushu.models import BaseDataModel
from shushu.storages.local_file import LocalFileStorage
from shushu.types import TypeId


def test_local_file_storage_perform_save_data_action(logger_fixture: MagicMock) -> None:
    class MyDataModel(BaseDataModel):
        type_id: TypeId = TypeId("01HW5QHEQ53AZ7HNNRM56RKD4P")
        some_value: int

    with TemporaryDirectory() as tempdir:
        storage = LocalFileStorage(path=Path(tempdir), logger=logger_fixture)
        my_data_base_dir = os.path.join(tempdir, "01HW5QHEQ53AZ7HNNRM56RKD4P")
        storage.perform(action=SaveDataAction(), payload=MyDataModel(some_value=123))
        fn = os.listdir(my_data_base_dir)[0]
        with open(os.path.join(my_data_base_dir, fn), "r", encoding="utf-8") as f:
            assert MyDataModel.model_validate_json(f.read()).some_value == 123
