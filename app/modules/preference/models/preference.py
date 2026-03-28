"""
偏好数据模型
"""

from sqlalchemy import Column, String, DateTime, Float, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from app.infrastructure.database import Base
from datetime import datetime, timezone
import uuid


class Preference(Base):
    __tablename__ = "preferences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    world_id = Column(String(50), nullable=True)  # 世界观级别偏好，可为空
    story_id = Column(UUID(as_uuid=True), ForeignKey("stories.id"), nullable=True)  # 故事级别偏好，可为空
    tag = Column(String(50), nullable=False)
    weight = Column(Float, default=1.0)  # 偏好权重
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        Index('idx_preference_user_tag', 'user_id', 'tag'),
        Index('idx_preference_user_world', 'user_id', 'world_id'),
    )