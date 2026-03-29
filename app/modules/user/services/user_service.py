"""
用户服务 - 个人主页、故事列表
"""

from uuid import UUID
from app.infrastructure.database import SessionLocal
from app.modules.user.models.user import User
from app.models.story import Story


class UserService:
    def __init__(self):
        self.db = SessionLocal()
    
    def get_profile(self, user_id: UUID) -> dict:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        
        # 获取故事数量
        story_count = self.db.query(Story).filter(Story.user_id == user_id).count()
        
        # 获取偏好标签（前5个）
        try:
            from app.modules.preference import PreferenceRecorder
            recorder = PreferenceRecorder(self.db)
            prefs = recorder.get_user_preferences(str(user_id), limit=5)
            favorite_tags = [p["tag"] for p in prefs]
        except:
            favorite_tags = []
        
        return {
            "user_id": str(user.id),
            "nickname": user.nickname,
            "avatar": user.avatar or "",
            "is_guest": user.is_guest,
            "story_count": story_count,
            "favorite_tags": favorite_tags
        }
    
    def update_profile(self, user_id: UUID, nickname: str = None, avatar: str = None) -> bool:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        if nickname:
            user.nickname = nickname
        if avatar:
            user.avatar = avatar
        
        self.db.commit()
        return True
    
    def get_user_stories(self, user_id: UUID) -> list:
        stories = self.db.query(Story).filter(
            Story.user_id == user_id
        ).order_by(Story.created_at.desc()).all()
        
        return [
            {
                "id": str(s.id),
                "title": s.title,
                "world": s.world.value,
                "summary": s.summary or "继续你的冒险...",
                "created_at": s.created_at.isoformat(),
                "status": s.status.value if s.status else "active"
            }
            for s in stories
        ]
    
    def close(self):
        self.db.close()