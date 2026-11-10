from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.models.chunk import Chunk

class Document(Base):
    __tablename__ = "documents"
    id: Mapped[int] = mapped_column(primary_key=True)
    document_key: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    filename: Mapped[str] = mapped_column(String(255))
    title: Mapped[str] = mapped_column(String(255))
    document_type: Mapped[str] = mapped_column(String(80), default="unknown")
    device_model: Mapped[str] = mapped_column(String(150), default="unknown")
    software_version: Mapped[str] = mapped_column(String(150), default="unknown")
    category: Mapped[str] = mapped_column(String(100), default="general")
    status: Mapped[str] = mapped_column(String(30), default="active", index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    chunks: Mapped[list["Chunk"]] = relationship(back_populates="document", cascade="all, delete-orphan")
