from sqlalchemy import Column, String, DateTime, Text, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.infrastructure.database import Base
from datetime import datetime, timezone
from app.modules.user.models.user import User
import uuid
import enum

from app.models.turn import Turn


class WorldType(str, enum.Enum):
    cyberpunk = "cyberpunk"
    fantasy = "fantasy"
    noir = "noir"
    xianxia = "xianxia"
    strategy = "strategy"
    urban = "urban"
    cthulhu = "cthulhu"
    wasteland = "wasteland"


class StoryStatus(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"


class Story(Base):
    __tablename__ = "stories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=True)
    title = Column(String(200), nullable=False)
    world = Column(Enum(WorldType), nullable=False)
    summary = Column(Text, nullable=True)
    status = Column(Enum(StoryStatus), default=StoryStatus.ACTIVE)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    turns = relationship("Turn", back_populates="story", cascade="all, delete-orphan")