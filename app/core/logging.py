import logging


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {"default": {"format": "-----> %(asctime)s | %(levelname)s | %(name)s | %(message)s"}},

    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "default"}},

    "loggers": {
        "": {"handlers": ["console"], "level": "INFO"},
        "app": {"handlers": ["console"], "level": "INFO", "propagate": False},
    }
}


def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
