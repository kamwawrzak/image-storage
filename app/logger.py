import logging
import sys
from .config import Config


def get_logger(config: Config) -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(config.log_level)
    stream_handler = logging.StreamHandler(sys.stdout)
    log_formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s")  
    stream_handler.setFormatter(log_formatter)
    logger.addHandler(stream_handler)
    return logger
