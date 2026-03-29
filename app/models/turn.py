from sqlalchemy import Column, String, DateTime, Text, Integer, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.infrastructure.database import Base
from datetime import datetime, timezone
import uuid


class Turn(Base):
    __tablename__ = "turns"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    story_id = Column(UUID(as_uuid=True), ForeignKey("stories.id"), nullable=False)
    turn_number = Column(Integer, nullable=False)
    narrative = Column(Text, nullable=False)
    choices = Column(Text, nullable=True)
    user_choice = Column(String(500), nullable=True)
    preference_tags = Column(JSON, nullable=True, default=list)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    story = relationship("app.models.story.Story", back_populates="turns")