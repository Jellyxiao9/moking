from app.infrastructure.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    new_values = ['cthulhu', 'wasteland']
    for val in new_values:
        try:
            conn.execute(text(f"ALTER TYPE worldtype ADD VALUE '{val}'"))
            print(f'✅ 添加 {val}')
        except Exception as e:
            if 'already exists' in str(e):
                print(f'⚠️ {val} 已存在，跳过')
            else:
                print(f'错误: {e}')
    conn.commit()
    print('✅ 枚举更新完成')