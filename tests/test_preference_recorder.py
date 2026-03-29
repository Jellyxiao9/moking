"""
测试偏好记录器
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.modules.preference import PreferenceRecorder
from app.modules.user.models.user import User
from app.infrastructure.database import SessionLocal
from app.repositories.story_repo import StoryRepo
import uuid

def test_recorder():
    db = SessionLocal()
    recorder = PreferenceRecorder(db)
    story_repo = StoryRepo(db)
    
    # 先创建一个测试用户
    test_user = User(
        id=uuid.uuid4(),
        nickname="测试用户",
        is_guest=True
    )
    db.add(test_user)
    db.commit()
    print(f"创建用户 ID: {test_user.id}")
    
    # 创建故事
    story = story_repo.create(title="测试故事", world="noir")
    print(f"创建故事 ID: {story.id}")
    
    # 记录偏好
    tags = ["调查", "硬汉"]
    print(f"记录偏好: {tags}")
    recorder.record(str(test_user.id), "noir", str(story.id), tags)
    
    # 获取偏好
    prefs = recorder.get_user_preferences(str(test_user.id))
    print(f"用户偏好: {prefs}")
    
    # 再次记录相同标签，测试衰减
    print("\n再次记录相同标签...")
    recorder.record(str(test_user.id), "noir", str(story.id), tags)
    
    prefs2 = recorder.get_user_preferences(str(test_user.id))
    print(f"更新后偏好: {prefs2}")
    
    recorder.close()
    db.close()

if __name__ == "__main__":
    test_recorder()