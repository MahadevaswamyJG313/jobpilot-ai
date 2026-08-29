import logging

from app.core.logger import setup_logger
from app.database.base import Base
from app.database.session import engine

# Import models so SQLAlchemy registers them
from app.models import Job  # noqa: F401

setup_logger()
logger = logging.getLogger(__name__)


def create_database() -> None:
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized successfully.")


if __name__ == "__main__":
    create_database()