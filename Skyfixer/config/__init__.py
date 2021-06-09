import logging
import pathlib
from argparse import ArgumentParser
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import List

from ConfigFramework import BaseConfig
from ConfigFramework.loaders import CompositeLoader, EnvLoader, JsonLoader
from ConfigFramework.variables import BoolVar, ConfigVar, IntVar
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import AsyncAdaptedQueuePool

from Skyfixer.config import validators
from .defaults import defaults

parser = ArgumentParser(argument_default={
    "config_path": Path(__file__).parent / "config.json",
    "create_config": False
})
parser.add_argument(
    "--config", "-c", action="store", dest="config_path",
    default=Path(__file__).parent / "config.json", type=Path
)
parser.add_argument("--make-config", "--new-config", action="store_true", dest="create_config", default=False)


launch_args, unknown = parser.parse_known_args()
if not launch_args.config_path.is_file() and not launch_args.create_config:
    raise ValueError("[--config] launch argument accepts path to config file only")

config_path: Path = launch_args.config_path

if launch_args.create_config:
    # Creates minimum json config
    config_path.write_text("{}")
    json_loader = JsonLoader.load(config_path, defaults=defaults)
    json_loader.dump(include_defaults=True)
    print(f"Created new config at {config_path}")
    exit(0)

json_loader = JsonLoader.load(config_path, defaults=defaults)
env_loader = EnvLoader.load()
composite_loader = CompositeLoader.load(env_loader, json_loader)


class SkyfixerConfig(BaseConfig):
    token = ConfigVar("skyfixer_token", composite_loader, caster=str, constant=True)
    default_prefix = ConfigVar("default_prefix", composite_loader, caster=str, validator=validators.validate_prefix)


class SkyfixerDBConfig(BaseConfig):
    db_uri = ConfigVar("db/connection_uri", composite_loader, default="sqlite+aiosqlite://data/skyfixer.db")
    pool_size = IntVar("db/pool_size", json_loader, default=15, validator=lambda v: v >= 0)
    max_overflow = IntVar("db/max_overflow", json_loader, default=0, validator=lambda v: v >= 0)
    kwargs = ConfigVar("db/kwargs", json_loader, default={})

    def __post_init__(self, *args, **kwargs):
        self.kwargs.value.pop('pool_size', None)
        self.kwargs.value.pop('max_overflow', None)
        self.kwargs.value.pop('poolclass', None)

        if self.db_uri.value == "sqlite+aiosqlite://data/skyfixer.db":
            db_base_path = Path(__file__).parent.parent / "data"
            db_base_path.mkdir(exist_ok=True)

        self.async_base_engine = create_async_engine(
            self.db_uri.value,
            poolclass=AsyncAdaptedQueuePool,
            pool_size=self.pool_size.value,
            max_overflow=self.max_overflow.value,
            **self.kwargs.value,
        )


class SkyfixerLogsConfig(BaseConfig):
    logs_dir = ConfigVar(
        "logs/directory", json_loader, default=Path(__file__).parent.parent / "logs",
        caster=Path
    )
    date_format = ConfigVar("logs/date_format", json_loader, validator=datetime.now().strftime, constant=True)
    log_format = ConfigVar("logs/format", json_loader, caster=logging.Formatter, constant=True)
    skyfixer_log_level = ConfigVar(
        "logs/skyfixer_log_level", json_loader, caster=lambda level: getattr(logging, level), constant=True
    )

    class LogsRotationConfig(BaseConfig):
        when = ConfigVar("logs/rotation/when", json_loader, constant=True)
        interval = IntVar("logs/rotation/interval", json_loader, validator=lambda v: v >= 1, constant=True)
        backup_count = IntVar("logs/rotation/backupCount", json_loader, validator=lambda v: v >= 1, constant=True)
        encoding = ConfigVar(
            "logs/rotation/encoding", json_loader, validator=validators.validate_encoding,
            default='utf-8', constant=True
        )
        utc_time = BoolVar("logs/rotation/utc", json_loader, default=True, constant=True)

    def __post_init__(self, *args, **kwargs) -> None:
        self.logs_dir.value.mkdir(exist_ok=True)
        self.logger = logging.getLogger("Skyfixer")
        handler = TimedRotatingFileHandler(
            filename=self.logs_dir.value / "skyfixer.log",
            when=self.LogsRotationConfig.when.value,
            interval=self.LogsRotationConfig.interval.value,
            backupCount=self.LogsRotationConfig.backup_count.value,
            encoding=self.LogsRotationConfig.encoding.value,
            utc=self.LogsRotationConfig.utc_time.value
        )
        self.logger.setLevel(self.skyfixer_log_level.value)
        self.logger.addHandler(handler)


class SkyfixerLocalisation(BaseConfig):
    locales_dir = ConfigVar("locales_dir", composite_loader, caster=Path, validator=Path.is_dir)
    supported_languages = ConfigVar("supported_languages", json_loader, caster=list)
    reference_language = ConfigVar("reference_language", json_loader, default="en")

    def __post_init__(self, *args, **kwargs):
        self.supported_languages_files: List[Path] = []

        for lang in self.supported_languages.value:
            filepath: Path = self.locales_dir.value / f"{lang}.json"

            if not filepath.is_file():
                raise ValueError(f"{lang} is not a language file in {filepath}")
            self.supported_languages_files.append(filepath)


skyfixer_config = SkyfixerConfig()
skyfixer_db_config = SkyfixerDBConfig()
skyfixer_logs_config = SkyfixerLogsConfig()
skyfixer_localisation = SkyfixerLocalisation()
logger = skyfixer_logs_config.logger

__all__ = ["skyfixer_config", "skyfixer_db_config", "skyfixer_logs_config", "skyfixer_localisation", "logger"]
