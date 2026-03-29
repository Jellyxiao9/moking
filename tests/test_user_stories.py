"""
测试用户故事 API
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.infrastructure.database import SessionLocal
from app.models.story import Story
from app.modules.user.models.user import User

def test_user_stories():
    db = SessionLocal()
    
    # 使用测试用户ID
    user_id = "6bd7bdf8-07b5-4141-8a8e-1c9d0f6e2e09"
    
    print(f"查询用户: {user_id}")
    
    # 检查用户是否存在
    user = db.query(User).filter(User.id == user_id).first()
    print(f"用户存在: {user is not None}")
    if user:
        print(f"用户名: {user.nickname}")
    
    # 查询故事
    try:
        stories = db.query(Story).filter(Story.user_id == user_id).all()
        print(f"故事数量: {len(stories)}")
        for s in stories:
            print(f"  - {s.title}")
    except Exception as e:
        print(f"查询失败: {e}")
    
    db.close()

if __name__ == "__main__":
    test_user_stories()