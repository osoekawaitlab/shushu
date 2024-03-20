from logging import FileHandler, Logger, StreamHandler, getLogger

from json_log_formatter import JSONFormatter

from .settings import LoggerSettings

LoggerLevelT = int


def get_logger(settings: LoggerSettings) -> Logger:
    """
    Get a logger with the given settings.

    :param settings: Logger settings
    :return: Logger

    >>> from shushu.settings import LoggerSettings
    >>> settings = LoggerSettings()
    >>> actual = get_logger(settings=settings)
    >>> actual
    <Logger shushu.logger (INFO)>
    >>> actual.handlers
    [<StreamHandler <stderr> (INFO)>]
    >>> import logging
    >>> import tempfile
    >>> with tempfile.NamedTemporaryFile() as temp:
    ...   settings2 = LoggerSettings(level=logging.WARNING, file_path=temp.name)
    ...   actual2 = get_logger(settings=settings2)
    ...   actual2
    <Logger shushu.logger (WARNING)>
    >>> actual2.handlers
    [<StreamHandler <stderr> (WARNING)>, <FileHandler ... (WARNING)>]
    """
    logger = getLogger(__name__)
    logger.setLevel(level=settings.level)
    formatter = JSONFormatter()

    for handler in logger.handlers:
        logger.removeHandler(handler)

    stream_handler = StreamHandler()
    stream_handler.setLevel(level=settings.level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if settings.file_path is not None:
        file_handler = FileHandler(filename=settings.file_path)
        file_handler.setLevel(level=settings.level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger
