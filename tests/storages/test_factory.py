from unittest.mock import MagicMock

from pytest_mock import MockerFixture

from shushu.settings import LocalFileStorageSettings
from shushu.storages.factory import StorageFactory


def test_factory_create_local_file_storage(logger_fixture: MagicMock, mocker: MockerFixture) -> None:
    LocalFileStorage = mocker.patch("shushu.storages.factory.LocalFileStorage")
    settings = LocalFileStorageSettings(path="path")
    actual = StorageFactory(logger=logger_fixture).create(settings=settings)
    assert actual == LocalFileStorage.return_value
    LocalFileStorage.assert_called_once_with(path=settings.path, logger=logger_fixture)
