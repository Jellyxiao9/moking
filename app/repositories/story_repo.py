"""
故事仓储层 - 管理故事会话的数据库操作
"""

from sqlalchemy.orm import Session
from uuid import UUID
from app.infrastructure.database import get_db
from app.models.story import Story, WorldType, StoryStatus


class StoryRepo:
    """故事仓储"""

    def __init__(self, db: Session = None):
        self.db = db or next(get_db())

    def create(self, title: str, world: str) -> Story:
        """创建新故事"""
        story = Story(
            title=title,
            world=WorldType(world),  # 转换为枚举
            summary="",  # 初始为空，后续可更新
            status="active"
        )
        self.db.add(story)
        self.db.commit()
        self.db.refresh(story)
        return story

    def get_by_id(self, story_id: UUID) -> Story | None:
        """根据ID获取故事"""
        return self.db.query(Story).filter(Story.id == story_id).first()

    def get_by_user(self, user_id: UUID) -> list[Story]:
        """获取指定用户的所有故事（按更新时间倒序）"""
        return self.db.query(Story).filter(
            Story.user_id == user_id
        ).order_by(Story.updated_at.desc()).all()

    def get_all(self, limit: int = 10) -> list[Story]:
        """获取所有故事（按更新时间倒序）"""
        return self.db.query(Story).order_by(
            Story.updated_at.desc()
        ).limit(limit).all()

    def update_summary(self, story_id: UUID, summary: str) -> None:
        """更新故事摘要"""
        story = self.get_by_id(story_id)
        if story:
            story.summary = summary
            self.db.commit()