LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s [%(asctime)s] [%(name)s] - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout"
        }
    },
    "loggers": {
        "": {
            "handlers": ["default"],
            "level": "WARNING",
            "propagate": True
        },

        "app": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": True
        },

        "app.auth_routes": {
            "handlers": ["default"],
            "level": "WARNING",
            "propagate": True
        },

        "app.db": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": True
        },
    }
}
