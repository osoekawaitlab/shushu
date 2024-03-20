from enum import Enum
from logging import INFO
from typing import Optional, Union

from oltl import TypeStringEnum
from oltl.settings import BaseSettings as OltlBaseSettings
from pydantic import Field, FilePath, NewPath
from pydantic_settings import SettingsConfigDict
from typing_extensions import Annotated

NewOrExistingPath = Annotated[Union[NewPath, FilePath], "NewOrExistingPath"]


class BaseSettings(OltlBaseSettings):
    model_config = SettingsConfigDict(env_prefix="SHUSHU_")


class LoggerSettings(BaseSettings):
    """
    Logger settings

    level: int = INFO
        Logging level

    file_path: Optional[NewOrExistingPath] = None
        File path to write logs to. Set if you want to write logs to a file.

    >>> LoggerSettings()
    LoggerSettings(level=20, file_path=None)
    >>> LoggerSettings(level=10, file_path="logs.log")
    LoggerSettings(level=10, file_path=PosixPath('logs.log'))
    """

    level: int = Field(default=INFO)
    file_path: Optional[NewOrExistingPath] = Field(default=None)


class InterfaceType(TypeStringEnum):
    CLI = "cli"
    API = "api"


class GlobalSettings(BaseSettings):
    """
    Global settings

    logger: LoggerSettings = LoggerSettings()
        Logger settings

    >>> GlobalSettings()
    GlobalSettings(logger=LoggerSettings(level=20, file_path=None))
    >>> GlobalSettings(logger=LoggerSettings(level=10, file_path="logs.log"))
    GlobalSettings(logger=LoggerSettings(level=10, file_path=PosixPath('logs.log')))
    """

    logger: LoggerSettings = Field(default_factory=LoggerSettings)
