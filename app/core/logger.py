import logging
from pathlib import Path


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"


def setup_logger() -> None:
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Prevent duplicate handlers during reload
    if root_logger.handlers:
        root_logger.handlers.clear()

    # Console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File
    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)