from sqlalchemy import String, Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.db.base import Base

class Chunk(Base):
    __tablename__ = "chunks"
    id: Mapped[int] = mapped_column(primary_key=True)
    chunk_key: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id", ondelete="CASCADE"), index=True)
    parent_key: Mapped[str] = mapped_column(String(120), index=True)
    page_number: Mapped[int] = mapped_column(Integer, default=1)
    section: Mapped[str] = mapped_column(String(255), default="Unknown")
    content: Mapped[str] = mapped_column(Text)
    parent_content: Mapped[str] = mapped_column(Text)
    document: Mapped["Document"] = relationship(back_populates="chunks")
