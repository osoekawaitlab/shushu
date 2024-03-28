from logging import Logger
from typing import Generator
from unittest.mock import MagicMock

from pytest import fixture
from pytest_mock import MockerFixture


@fixture
def logger_fixture(mocker: MockerFixture) -> Generator[MagicMock, None, None]:
    yield mocker.MagicMock(spec=Logger)
