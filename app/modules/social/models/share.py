"""
分享模型
"""

from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from app.infrastructure.database import Base
from datetime import datetime, timezone
import uuid
import enum


class ShareType(str, enum.Enum):
    ENDING = "ending"
    SCREENSHOT = "screenshot"
    LINK = "link"


class Share(Base):
    __tablename__ = "shares"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    story_id = Column(UUID(as_uuid=True), ForeignKey("stories.id"), nullable=False)
    share_type = Column(SQLEnum(ShareType), default=ShareType.ENDING)
    share_url = Column(String(500), nullable=False)
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))