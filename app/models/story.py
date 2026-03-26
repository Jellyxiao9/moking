from sqlalchemy import Column, String, DateTime, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.infrastructure.database import Base
from datetime import datetime, timezone
import uuid
import enum


class WorldType(str, enum.Enum):
    cyberpunk = "cyberpunk"
    fantasy = "fantasy"
    noir = "noir"


class Story(Base):
    __tablename__ = "stories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    world = Column(Enum(WorldType), nullable=False)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    turns = relationship("Turn", back_populates="story", cascade="all, delete-orphan")