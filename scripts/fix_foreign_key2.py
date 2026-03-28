"""
修复 stories.user_id 外键
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.infrastructure.database import engine
from sqlalchemy import text


def fix_foreign_key():
    with engine.connect() as conn:
        # 先删除外键
        conn.execute(text('ALTER TABLE stories DROP CONSTRAINT IF EXISTS fk_stories_user_id'))
        conn.execute(text('ALTER TABLE stories DROP CONSTRAINT IF EXISTS stories_user_id_fkey'))
        conn.commit()
        print("已删除旧外键")
        
        # 确保 users 表存在
        result = conn.execute(text("SELECT EXISTS (SELECT 1 FROM pg_tables WHERE tablename='users')"))
        users_exists = result.fetchone()[0]
        print(f'users 表存在: {users_exists}')
        
        if not users_exists:
            print("❌ users 表不存在，请先运行迁移")
            return
        
        # 重新创建外键
        conn.execute(text("""
            ALTER TABLE stories 
            ADD CONSTRAINT fk_stories_user_id 
            FOREIGN KEY (user_id) 
            REFERENCES users(id)
            ON DELETE SET NULL
        """))
        conn.commit()
        print('✅ 外键修复完成')


if __name__ == "__main__":
    fix_foreign_key()