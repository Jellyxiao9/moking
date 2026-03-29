"""
检查 preferences 表结构
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.infrastructure.database import engine
from sqlalchemy import text

def test_preferences_columns():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='preferences'"))
        columns = [row[0] for row in result]
        print('preferences 表列:', columns)
        
        expected = ['id', 'user_id', 'world_id', 'story_id', 'tag', 'weight', 'updated_at', 'created_at']
        for col in expected:
            if col in columns:
                print(f"  ✅ {col}")
            else:
                print(f"  ❌ {col} 缺失")

if __name__ == "__main__":
    test_preferences_columns()