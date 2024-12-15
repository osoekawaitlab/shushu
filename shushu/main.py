import os
from argparse import ArgumentParser

from ollogger import get_logger

from . import __version__
from .core import gen_shushu_core
from .interfaces.factory import InterfaceFactory
from .settings import GlobalSettings


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--version", action="version", version=f"shushu {__version__}")
    parser.add_argument("--config-env-file-path", type=str, help="Path to the configuration env file")
    parser.add_argument("target", type=str, help="The target url to scrape")

    args = parser.parse_args()

    config_file_env = args.config_env_file_path
    if config_file_env is None:
        config_file_env = os.getenv("SHUSHU_CONFIG_ENV_FILE_PATH", ".env")
    global_settings = GlobalSettings(_env_file=config_file_env)
    logger = get_logger(settings=global_settings.logger_settings)
    logger.info("global settings", extra={"global_settings": global_settings.model_dump()})
    shushu_core = gen_shushu_core(settings=global_settings.core_settings, logger=logger)
    interface = InterfaceFactory(core=shushu_core, logger=logger).create(settings=global_settings.interface_settings)
    interface.run(target=args.target)
