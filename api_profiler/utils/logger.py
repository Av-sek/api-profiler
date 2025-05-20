import logging
import logging.config

from api_profiler.utils.log_sql import LogColors

class LogColorsFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: LogColors.CYAN,
        logging.INFO: LogColors.GREEN,
        logging.WARNING: LogColors.YELLOW,
        logging.ERROR: LogColors.MAGENTA,
        logging.CRITICAL: LogColors.BOLD + LogColors.MAGENTA,
    }

    def format(self, record):
        color = self.COLORS.get(record.levelno, LogColors.RESET)
        record.levelname = color + record.levelname + LogColors.RESET
        message = super().format(record)
        return message
    
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,  # Keep existing loggers working
    "formatters": {
        "default": {
            "()": LogColorsFormatter,
            "format": "[%(levelname)s] %(asctime)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "DEBUG",
            "stream": "ext://sys.stdout",  # Output to console
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
        "console": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    }
}

# Apply the configuration
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("console")

def silence_django_server_logs():
    """
    Silences Django's default 'django.server' logger, which logs every HTTP request.
    """
    logger = logging.getLogger("django.server")
    logger.handlers.clear()        # Remove any handlers (like StreamHandler)
    logger.setLevel(logging.CRITICAL)  # Raise the threshold to only show critical issues
    logger.propagate = False       # Prevent bubbling up to root logger