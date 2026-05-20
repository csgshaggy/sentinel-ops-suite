import logging
import sys

from utils.settings import Settings

settings = Settings()


class ColorFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[36m",
        "INFO": "\033[32m",
        "WARNING": "\033[33m",
        "ERROR": "\033[31m",
        "CRITICAL": "\033[41m",
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelname, "")
        message = super().format(record)
        return f"{color}{message}{self.RESET}"


def init_logging():
    handler = logging.StreamHandler(sys.stdout)

    if settings.log_json:
        # JSON structured logs
        import json_log_formatter

        handler.setFormatter(json_log_formatter.JSONFormatter())
    else:
        # Color logs
        handler.setFormatter(ColorFormatter("[%(levelname)s] %(message)s"))

    logging.basicConfig(
        level=settings.log_level,
        handlers=[handler],
        force=True,
    )
