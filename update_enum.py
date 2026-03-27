from app.infrastructure.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TYPE worldtype ADD VALUE 'xianxia'"))
        conn.execute(text("ALTER TYPE worldtype ADD VALUE 'strategy'"))
        conn.execute(text("ALTER TYPE worldtype ADD VALUE 'urban'"))
        conn.commit()
        print('✅ 枚举类型更新成功')
    except Exception as e:
        if 'already exists' in str(e):
            print('⚠️ 枚举值已存在，跳过')
        else:
            print(f'错误: {e}')