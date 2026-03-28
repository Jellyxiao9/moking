"""
修改 storystatus 枚举为大写
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.infrastructure.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    # 开始事务
    trans = conn.begin()
    try:
        # 修改枚举值
        conn.execute(text("ALTER TYPE storystatus RENAME TO storystatus_old"))
        conn.execute(text("CREATE TYPE storystatus AS ENUM('ACTIVE', 'COMPLETED')"))
        conn.execute(text("ALTER TABLE stories ALTER COLUMN status TYPE storystatus USING status::text::storystatus"))
        conn.execute(text("DROP TYPE storystatus_old"))
        trans.commit()
        print('✅ 枚举类型已更新为大写')
    except Exception as e:
        trans.rollback()
        print(f'❌ 失败: {e}')