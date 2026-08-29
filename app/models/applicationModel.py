from datetime import datetime
from sqlalchemy import DateTime, Integer, Enum, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.common.enums import ApplicationStatus


class JobApplication(Base):
    __tablename__ = "job_applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    job_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus), default=ApplicationStatus.SAVED, nullable=False
    )
    applied_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Cascading and parent linkage routing
    job = relationship("Job", back_populates="application")
