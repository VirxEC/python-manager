import logging
import sys

DEFAULT_LOGGER_NAME = "rlbot"
DEFAULT_LOGGER = None
LOGGING_LEVEL = logging.INFO

logging.getLogger().setLevel(logging.NOTSET)


class CustomFormatter(logging.Formatter):
    GREY = "\x1b[38;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"
    FORMAT = "%(asctime)s %(levelname)s:%(name)5s[%(filename)20s:%(lineno)s - %(funcName)20s() ] %(message)s"

    FORMATS = {
        logging.DEBUG: GREY + FORMAT + RESET,
        logging.INFO: GREY + FORMAT + RESET,
        logging.WARNING: YELLOW + FORMAT + RESET,
        logging.ERROR: RED + FORMAT + RESET,
        logging.CRITICAL: BOLD_RED + FORMAT + RESET,
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_logger(logger_name: str, log_creation: bool=True) -> logging.Logger:
    if logger_name == DEFAULT_LOGGER_NAME and DEFAULT_LOGGER is not None:
        return DEFAULT_LOGGER

    logger = logging.getLogger(logger_name)
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setFormatter(CustomFormatter())
        ch.setLevel(LOGGING_LEVEL)
        logger.addHandler(ch)
    logging.getLogger().handlers = []

    if log_creation:
        logger.debug("creating logger for %s", sys._getframe().f_back)
    return logger


DEFAULT_LOGGER = get_logger(DEFAULT_LOGGER_NAME, log_creation=False)
