from enum import Enum
from logging import INFO
from typing import Literal, Optional, TypeVar, Union

from oltl.settings import BaseSettings as OltlBaseSettings
from pydantic import DirectoryPath, Field, FilePath, NewPath
from pydantic_settings import SettingsConfigDict
from typing_extensions import Annotated

NewOrExistingPath = Annotated[Union[NewPath, FilePath], "NewOrExistingPath"]
NewOrExistingDirectoryPath = Annotated[Union[DirectoryPath, NewPath], "NewOrExistingDirectoryPath"]
SettingsT = TypeVar("SettingsT", bound="BaseSettings")


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


class InterfaceType(str, Enum):
    CLI = "CLI"


class BaseInterfaceSettings(BaseSettings):
    type: InterfaceType


class CliInterfaceSettings(BaseInterfaceSettings):
    type: Literal[InterfaceType.CLI] = InterfaceType.CLI


InterfaceSettings = Annotated[CliInterfaceSettings, Field(discriminator="type")]


class WebAgentType(str, Enum):
    SELENIUM = "SELENIUM"


class BaseWebAgentSettings(BaseSettings):
    type: WebAgentType


class SeleniumDriverType(str, Enum):
    CHROME = "CHROME"


class BaseSeleniumDriverSettings(BaseSettings):
    type: SeleniumDriverType


class ChromeSeleniumDriverSettings(BaseSeleniumDriverSettings):
    type: Literal[SeleniumDriverType.CHROME] = SeleniumDriverType.CHROME


SeleniumDriverSettings = Annotated[ChromeSeleniumDriverSettings, Field(discriminator="type")]


class SeleniumWebAgentSettings(BaseWebAgentSettings):
    type: Literal[WebAgentType.SELENIUM] = WebAgentType.SELENIUM
    driver_settings: SeleniumDriverSettings = Field(default_factory=ChromeSeleniumDriverSettings)


WebAgentSettings = Annotated[SeleniumWebAgentSettings, Field(discriminator="type")]


class StorageType(str, Enum):
    LOCAL_FILE = "LOCAL_FILE"


class BaseStorageSettings(BaseSettings):
    type: StorageType


class LocalFileStorageSettings(BaseStorageSettings):
    type: Literal[StorageType.LOCAL_FILE] = StorageType.LOCAL_FILE
    path: NewOrExistingDirectoryPath


StorageSettings = Annotated[LocalFileStorageSettings, Field(discriminator="type")]


class CoreSettings(BaseSettings):
    web_agent_settings: WebAgentSettings = Field(default_factory=SeleniumWebAgentSettings)
    storage_settings: StorageSettings = Field(default_factory=lambda: LocalFileStorageSettings(path="."))


class GlobalSettings(BaseSettings):
    """
    Global settings

    logger: LoggerSettings = LoggerSettings()
        Logger settings

    """  # noqa: E501

    logger_settings: LoggerSettings = Field(default_factory=LoggerSettings)
    interface_settings: InterfaceSettings = Field(default_factory=CliInterfaceSettings)
    core_settings: CoreSettings = Field(default_factory=CoreSettings)
