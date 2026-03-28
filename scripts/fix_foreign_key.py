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
        # 检查外键是否存在
        result = conn.execute(text("""
            SELECT conname 
            FROM pg_constraint 
            WHERE conrelid = 'stories'::regclass 
            AND contype = 'f'
        """))
        fks = [row[0] for row in result]
        print(f"现有外键: {fks}")
        
        # 如果有外键，先删除
        for fk in fks:
            if 'user_id' in fk:
                print(f"删除外键: {fk}")
                conn.execute(text(f"ALTER TABLE stories DROP CONSTRAINT {fk}"))
        
        # 重新添加外键
        conn.execute(text("""
            ALTER TABLE stories 
            ADD CONSTRAINT fk_stories_user_id 
            FOREIGN KEY (user_id) 
            REFERENCES users(id)
        """))
        conn.commit()
        print("✅ 外键已修复")


if __name__ == "__main__":
    fix_foreign_key()