"""
社交分享服务
"""

from uuid import UUID
from datetime import datetime, timezone
from app.infrastructure.database import SessionLocal
from app.modules.social.models.share import Share, ShareType
from app.models.story import Story
from app.modules.user.models.user import User


class SocialService:
    def __init__(self):
        self.db = SessionLocal()
    
    def create_share(self, story_id: UUID, user_id: UUID, share_type: str = "ending") -> dict:
        """创建分享"""
        # 验证故事存在
        story = self.db.query(Story).filter(Story.id == story_id).first()
        if not story:
            return None
        
        # 验证用户存在
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        
        # 生成分享ID
        import uuid
        share_id = uuid.uuid4()
        
        # 生成分享链接
        share_url = f"/share/{share_id}"
        
        share = Share(
            id=share_id,
            user_id=user_id,
            story_id=story_id,
            share_type=ShareType(share_type),
            share_url=share_url,
            view_count=0
        )
        
        self.db.add(share)
        self.db.commit()
        self.db.refresh(share)
        
        return {
            "share_id": str(share.id),
            "share_url": share.share_url,
            "created_at": share.created_at.isoformat()
        }
    
    def get_share(self, share_id: UUID) -> dict:
        """获取分享内容"""
        share = self.db.query(Share).filter(Share.id == share_id).first()
        if not share:
            return None
        
        # 获取故事详情
        story = self.db.query(Story).filter(Story.id == share.story_id).first()
        user = self.db.query(User).filter(User.id == share.user_id).first()
        
        return {
            "share_id": str(share.id),
            "story": {
                "id": str(story.id),
                "title": story.title,
                "world": story.world.value,
                "summary": story.summary,
                "created_at": story.created_at.isoformat()
            },
            "user": {
                "nickname": user.nickname,
                "avatar": user.avatar
            },
            "share_type": share.share_type.value,
            "view_count": share.view_count,
            "created_at": share.created_at.isoformat()
        }
    
    def get_user_shares(self, user_id: UUID) -> list:
        """获取用户的所有分享"""
        shares = self.db.query(Share).filter(
            Share.user_id == user_id
        ).order_by(Share.created_at.desc()).all()
        
        return [
            {
                "share_id": str(s.id),
                "story_title": self.db.query(Story).filter(Story.id == s.story_id).first().title,
                "share_type": s.share_type.value,
                "view_count": s.view_count,
                "created_at": s.created_at.isoformat()
            }
            for s in shares
        ]
    
    def increment_view_count(self, share_id: UUID):
        """增加浏览次数"""
        share = self.db.query(Share).filter(Share.id == share_id).first()
        if share:
            share.view_count += 1
            self.db.commit()
    
    def close(self):
        self.db.close()