"""
创建默认系统用户，用于关联现有无主故事
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.infrastructure.database import SessionLocal
from app.modules.user.models.user import User, UserStatus
import uuid


def create_default_user():
    db = SessionLocal()
    
    try:
        # 检查是否已存在
        existing = db.query(User).filter(User.nickname == "系统用户").first()
        if existing:
            print("✅ 默认用户已存在")
            return existing.id
        
        # 创建默认用户
        default_user = User(
            id=uuid.uuid4(),
            phone=None,
            password_hash=None,
            nickname="系统用户",
            is_guest=True,
            status=UserStatus.ACTIVE,
            free_generations_today=999
        )
        db.add(default_user)
        db.commit()
        db.refresh(default_user)
        
        print(f"✅ 创建默认用户成功，ID: {default_user.id}")
        return default_user.id
        
    except Exception as e:
        print(f"❌ 创建默认用户失败: {e}")
        db.rollback()
        return None
    finally:
        db.close()


if __name__ == "__main__":
    create_default_user()