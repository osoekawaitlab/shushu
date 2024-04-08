from contextlib import AbstractContextManager
from logging import Logger
from types import TracebackType

from oltl import BaseModel

from .base import BaseShushuComponent
from .data_processors.factory import DataProcessorFactory
from .exceptions import MemoryNotSetError
from .models import (
    CoreAction,
    DataProcessorCoreAction,
    MemoryPayload,
    StorageCoreAction,
    WebAgentCoreAction,
)
from .settings import CoreSettings
from .storages.base import BaseStorage
from .storages.factory import StorageFactory
from .web_agents.base import BaseWebAgent
from .web_agents.factory import WebAgentFactory


class ShushuCore(BaseShushuComponent, AbstractContextManager["ShushuCore"]):
    def __init__(self, logger: Logger, web_agent: BaseWebAgent, storage: BaseStorage) -> None:
        super(ShushuCore, self).__init__(logger=logger)
        self._web_agent = web_agent
        self._storage = storage
        self._memroy: None | BaseModel = None

    @property
    def web_agent(self) -> BaseWebAgent:
        return self._web_agent

    @property
    def storage(self) -> BaseStorage:
        return self._storage

    def set_memory(self, memory: BaseModel) -> None:
        self._memroy = memory

    def get_memory(self) -> BaseModel:
        if self._memroy is None:
            raise MemoryNotSetError()
        return self._memroy

    def __enter__(self) -> "ShushuCore":
        self.web_agent.__enter__()
        return self

    def __exit__(
        self,
        __exc_type: type[BaseException] | None,
        __exc_value: BaseException | None,
        __traceback: TracebackType | None,
    ) -> bool | None:
        self.web_agent.__exit__(__exc_type, __exc_value, __traceback)
        return None

    def perform(self, action: CoreAction) -> None:
        if isinstance(action, WebAgentCoreAction):
            self.web_agent.perform(action.action)
            return
        if isinstance(action, StorageCoreAction):
            if action.payload is None:
                self.storage.perform(action=action.action)
                return
            if isinstance(action.payload, MemoryPayload):
                self.storage.perform(action=action.action, payload=self.get_memory())
                return
        if isinstance(action, DataProcessorCoreAction):
            data_processor_factory = DataProcessorFactory(logger=self.logger)
            data_processor = data_processor_factory.create(action=action.action, payload=self.get_memory())
            self.set_memory(data_processor.perform())
            return


def gen_shushu_core(settings: CoreSettings, logger: Logger) -> ShushuCore:
    web_agent_factory = WebAgentFactory(logger=logger)
    web_agent = web_agent_factory.create(settings=settings.web_agent_settings)
    storage_factory = StorageFactory(logger=logger)
    storage = storage_factory.create(settings=settings.storage_settings)
    return ShushuCore(logger=logger, web_agent=web_agent, storage=storage)
