defaults = {
    "skyfixer_token": "TOKEN",
    "default_prefix": "s!",

    "db": {
        "connection_uri": "sqlite+aiosqlite:///Skyfixer/data/skyfixer.db",
        "pool_size": 15,
        "max_overflow": 0,
        "kwargs": {}
    },

    "logs": {
        "directory": "./Skyfixer/logs/",
        "date_format": "%y%m%d %H:%M:%S",
        "format": "%(asctime)s - %(name)s - %(levelname)s: %(message)s",
        "skyfixer_log_level": "ERROR",
        "rotation": {
            "backupCount": "5",
            "encoding": "utf-8",
            "interval": 6,
            "utc": True,
            "when": "h",
        }
    },
    "locales_dir": "./Skyfixer/languages/",
    "supported_languages": ['en'],
    "reference_language": 'en',
}
