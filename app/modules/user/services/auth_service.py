"""
认证服务 - 注册、登录、游客
"""

import uuid
import hashlib
from app.infrastructure.database import SessionLocal
from app.modules.user.models.user import User, UserStatus


class AuthService:
    def __init__(self):
        self.db = SessionLocal()
    
    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register(self, phone: str, password: str, nickname: str) -> dict:
        # 检查手机号是否已存在
        existing = self.db.query(User).filter(User.phone == phone).first()
        if existing:
            return None
        
        user = User(
            id=uuid.uuid4(),
            phone=phone,
            password_hash=self._hash_password(password),
            nickname=nickname,
            is_guest=False,
            status=UserStatus.ACTIVE
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return {
            "user_id": str(user.id),
            "nickname": user.nickname,
            "is_guest": False
        }
    
    def login(self, phone: str, password: str) -> dict:
        user = self.db.query(User).filter(
            User.phone == phone,
            User.status == UserStatus.ACTIVE
        ).first()
        
        if not user or user.password_hash != self._hash_password(password):
            return None
        
        return {
            "user_id": str(user.id),
            "nickname": user.nickname,
            "is_guest": user.is_guest
        }
    
    def create_guest(self) -> uuid.UUID:
        guest_id = uuid.uuid4()
        user = User(
            id=guest_id,
            nickname=f"游客_{str(guest_id)[:8]}",
            is_guest=True,
            status=UserStatus.ACTIVE
        )
        self.db.add(user)
        self.db.commit()
        return guest_id
    
    def close(self):
        self.db.close()