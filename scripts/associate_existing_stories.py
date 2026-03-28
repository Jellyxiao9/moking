"""
将现有故事关联到默认用户
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.infrastructure.database import SessionLocal
from app.models.story import Story
from scripts.seed_default_user import create_default_user


def associate_stories():
    db = SessionLocal()
    
    try:
        # 确保默认用户存在
        user_id = create_default_user()
        
        # 找出没有 user_id 的故事
        orphan_stories = db.query(Story).filter(Story.user_id.is_(None)).all()
        
        if not orphan_stories:
            print("✅ 没有需要关联的故事")
            return
        
        print(f"找到 {len(orphan_stories)} 个无主故事")
        
        # 关联到默认用户
        for story in orphan_stories:
            story.user_id = user_id
            print(f"  关联故事: {story.title} ({story.id})")
        
        db.commit()
        print(f"✅ 已关联 {len(orphan_stories)} 个故事到系统用户")
        
    except Exception as e:
        print(f"❌ 关联失败: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    associate_stories()