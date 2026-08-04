from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from sqlalchemy import Enum

from app.common.enums import JobSource


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String(255), nullable=False)

    company_name: Mapped[str] = mapped_column(String(255), nullable=False)

    location: Mapped[str] = mapped_column(String(255), nullable=False)

    source: Mapped[JobSource] = mapped_column(Enum(JobSource),nullable=False,)

    job_url: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow,)

    updated_at: Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,)
    salary_min: Mapped[float | None] = mapped_column(Float,nullable=True,)

    salary_max: Mapped[float | None] = mapped_column(Float,nullable=True,)

    salary_currency: Mapped[str | None] = mapped_column(String(10),nullable=True,)

    salary_period: Mapped[str | None] = mapped_column(String(20),nullable=True,)
    is_remote: Mapped[bool] = mapped_column(default=False,)