"""
验证 Phase 2 表结构
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.infrastructure.database import engine
from sqlalchemy import text


def test_stories_columns():
    """验证 stories 表有新字段"""
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='stories'
        """))
        columns = [row[0] for row in result]
        
        expected = ['status', 'user_id']
        for col in expected:
            if col in columns:
                print(f"✅ stories 表有 {col} 列")
            else:
                print(f"❌ stories 表缺少 {col} 列")


def test_turns_columns():
    """验证 turns 表有新字段"""
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='turns'
        """))
        columns = [row[0] for row in result]
        
        if 'preference_tags' in columns:
            print("✅ turns 表有 preference_tags 列")
        else:
            print("❌ turns 表缺少 preference_tags 列")


def test_preferences_table():
    """验证 preferences 表已创建"""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT tablename FROM pg_tables WHERE tablename='preferences'"))
        exists = result.fetchone() is not None
        
        if exists:
            print("✅ preferences 表已创建")
            
            # 查看列
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='preferences'
            """))
            columns = [row[0] for row in result]
            print(f"   preferences 列: {columns}")
        else:
            print("❌ preferences 表不存在")


if __name__ == "__main__":
    print("=" * 50)
    print("Phase 2 验证")
    print("=" * 50)
    test_stories_columns()
    test_turns_columns()
    test_preferences_table()