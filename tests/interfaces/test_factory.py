from logging import Logger

from pytest_mock import MockerFixture

from shushu.core import ShushuCore
from shushu.interfaces.factory import InterfaceFactory
from shushu.settings import CliInterfaceSettings


def test_interaface_factory_creates_cli(mocker: MockerFixture) -> None:
    logger = mocker.MagicMock(spec=Logger)
    core = mocker.MagicMock(spec=ShushuCore)
    CliInterface = mocker.patch("shushu.interfaces.factory.CliInterface")
    settings = CliInterfaceSettings()
    actual = InterfaceFactory(core=core, logger=logger).create(settings=settings)
    assert CliInterface.return_value == actual
    CliInterface.assert_called_once_with(core=core, logger=logger)
