"""
偏好记录器 - 使用指数衰减加权算法记录用户偏好
"""

from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.infrastructure.database import SessionLocal
from app.modules.preference.models.preference import Preference
from app.models.turn import Turn


class PreferenceRecorder:
    """偏好记录器"""
    
    # 衰减系数：每次新选择后，旧权重衰减5%
    DECAY_RATE = 0.95
    
    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()
    
    def record(self, user_id: str, world_id: str, story_id: str, tags: list, turn_id: str = None):
        """
        记录偏好
        
        Args:
            user_id: 用户ID
            world_id: 世界观ID
            story_id: 故事ID
            tags: 本轮相关的标签列表
            turn_id: 轮次ID（可选）
        """
        if not tags:
            return
        
        for tag in tags:
            self._update_preference(user_id, world_id, story_id, tag)
    
    def _update_preference(self, user_id: str, world_id: str, story_id: str, tag: str):
        """更新单个偏好（指数衰减加权）"""
        # 查找现有偏好
        existing = self.db.query(Preference).filter(
            Preference.user_id == user_id,
            Preference.tag == tag
        ).first()
        
        if existing:
            # 指数衰减：新权重 = 旧权重 × 衰减系数 + 1
            new_weight = existing.weight * self.DECAY_RATE + 1
            existing.weight = new_weight
            existing.updated_at = datetime.now(timezone.utc)
        else:
            # 新增偏好，初始权重为1
            new_pref = Preference(
                user_id=user_id,
                world_id=world_id,
                story_id=story_id,
                tag=tag,
                weight=1.0
            )
            self.db.add(new_pref)
        
        self.db.commit()
    
    def get_user_preferences(self, user_id: str, limit: int = 10) -> list:
        """获取用户偏好标签（按权重排序）"""
        prefs = self.db.query(Preference).filter(
            Preference.user_id == user_id
        ).order_by(Preference.weight.desc()).limit(limit).all()
        
        return [{"tag": p.tag, "weight": p.weight} for p in prefs]
    
    def close(self):
        self.db.close()