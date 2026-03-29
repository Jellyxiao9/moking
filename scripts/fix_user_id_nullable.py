"""
修复 stories.user_id 允许为空
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.infrastructure.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    # 检查当前状态
    result = conn.execute(text("SELECT column_name, is_nullable FROM information_schema.columns WHERE table_name='stories'"))
    print("当前 stories 表列状态:")
    for row in result:
        print(f'  {row[0]}: is_nullable={row[1]}')
    
    # 修改为允许为空
    conn.execute(text("ALTER TABLE stories ALTER COLUMN user_id DROP NOT NULL"))
    conn.commit()
    print('\n✅ user_id 已允许为空')