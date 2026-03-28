"""
用户数据模型
"""

from sqlalchemy import Column, String, DateTime, Integer, Boolean, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from app.infrastructure.database import Base
from datetime import datetime, timezone
import uuid
import enum


class UserStatus(str, enum.Enum):
    ACTIVE = "active"
    BANNED = "banned"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone = Column(String(20), unique=True, nullable=True)
    password_hash = Column(String(255), nullable=True)
    nickname = Column(String(50), default="旅行者")
    avatar = Column(String(500), nullable=True)
    status = Column(SQLEnum(UserStatus), default=UserStatus.ACTIVE)
    is_guest = Column(Boolean, default=True)
    free_generations_today = Column(Integer, default=5)
    last_reset_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))