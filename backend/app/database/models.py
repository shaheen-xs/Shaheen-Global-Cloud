"""SQLAlchemy ORM models for Shaheen Global Cloud."""

import enum
import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    String, Integer, Enum, DateTime, ForeignKey, Text, Boolean,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class ServerStatus(str, enum.Enum):
    running = "running"
    stopped = "stopped"
    provisioning = "provisioning"
    error = "error"
    deleting = "deleting"


class JobType(str, enum.Enum):
    provision = "provision"
    destroy = "destroy"
    start = "start"
    stop = "stop"
    restart = "restart"


class JobStatus(str, enum.Enum):
    queued = "queued"
    running = "running"
    completed = "completed"
    failed = "failed"


class Server(Base):
    __tablename__ = "servers"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    hostname: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    plan: Mapped[str] = mapped_column(String(50), nullable=False, default="small")
    region: Mapped[str] = mapped_column(String(50), nullable=False, default="us-east-1")
    image: Mapped[str] = mapped_column(String(100), nullable=False, default="ubuntu-24.04")
    status: Mapped[ServerStatus] = mapped_column(
        Enum(ServerStatus), nullable=False, default=ServerStatus.provisioning,
    )
    ipv4: Mapped[str | None] = mapped_column(String(45), nullable=True)
    ipv6: Mapped[str | None] = mapped_column(String(100), nullable=True)
    cpu_cores: Mapped[int] = mapped_column(Integer, nullable=False, default=2)
    memory_mb: Mapped[int] = mapped_column(Integer, nullable=False, default=2048)
    disk_gb: Mapped[int] = mapped_column(Integer, nullable=False, default=40)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow,
    )

    jobs: Mapped[list["Job"]] = relationship("Job", back_populates="server", cascade="all, delete-orphan")


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    server_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("servers.id", ondelete="SET NULL"), nullable=True,
    )
    job_type: Mapped[JobType] = mapped_column(Enum(JobType), nullable=False)
    status: Mapped[JobStatus] = mapped_column(Enum(JobStatus), nullable=False, default=JobStatus.queued)
    message: Mapped[str] = mapped_column(Text, nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow,
    )

    server: Mapped[Server | None] = relationship("Server", back_populates="jobs")
