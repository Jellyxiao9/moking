"""
验证数据库表是否创建成功
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.infrastructure.database import engine
from sqlalchemy import text


def test_tables_exist():
    """验证所有预期表是否存在"""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT tablename FROM pg_tables WHERE schemaname='public'"))
        tables = [row[0] for row in result]
        
        expected_tables = ['stories', 'turns', 'users', 'guest_mappings']
        
        for table in expected_tables:
            if table in tables:
                print(f"✅ 表 {table} 存在")
            else:
                print(f"❌ 表 {table} 不存在")
        
        print(f"\n所有表: {tables}")


if __name__ == "__main__":
    test_tables_exist()