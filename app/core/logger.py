import logging
from pathlib import Path

from app.core.settings import settings

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

APP_LOG = LOG_DIR / "app.log"
ERROR_LOG = LOG_DIR / "error.log"


def setup_logger() -> None:
    root_logger = logging.getLogger()

    # Avoid duplicate handlers during reload
    if root_logger.handlers:
        root_logger.handlers.clear()

    root_logger.setLevel(getattr(logging, settings.log_level.upper()))

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )

    # -----------------------------
    # Console Handler
    # -----------------------------
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(formatter)

    # -----------------------------
    # Application Log
    # -----------------------------
    app_handler = logging.FileHandler(
        APP_LOG,
        encoding="utf-8",
    )
    app_handler.setLevel(logging.INFO)
    app_handler.setFormatter(formatter)

    # -----------------------------
    # Error Log
    # -----------------------------
    error_handler = logging.FileHandler(
        ERROR_LOG,
        encoding="utf-8",
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(app_handler)
    root_logger.addHandler(error_handler)