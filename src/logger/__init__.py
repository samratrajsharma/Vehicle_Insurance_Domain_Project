import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pathlib import Path

# -------------------------------------------------------------------
# Get project root:  logger/__init__.py -> src -> project root
# -------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOG_PATH = LOG_DIR / LOG_FILE

MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 3  # Number of backup log files to keep


def configure_logger():
    """
    Configures logging with a rotating file handler and a console handler.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # avoid adding handlers multiple times
    if logger.handlers:
        return

    formatter = logging.Formatter(
        "[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s"
    )

    # File handler with rotation
    file_handler = RotatingFileHandler(
        LOG_PATH,
        maxBytes=MAX_LOG_SIZE,
        backupCount=BACKUP_COUNT,
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Just to see where it's writing
    print("Logging to:", LOG_PATH)


# configure on import
configure_logger()

# so `from src.logger import logging` works
__all__ = ["logging"]
