"""add preference_tags, story_status, preferences table

Revision ID: cf6518a6b120
Revises: 22f779b8b933
Create Date: 2026-03-28 20:39:14.316704

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'cf6518a6b120'
down_revision: Union[str, Sequence[str], None] = '22f779b8b933'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 创建枚举类型
    op.execute("CREATE TYPE storystatus AS ENUM ('active', 'completed')")
    
    # 添加列
    op.add_column('stories', sa.Column('status', sa.Enum('active', 'completed', name='storystatus'), nullable=True))
    op.add_column('turns', sa.Column('preference_tags', sa.JSON(), nullable=True))
    
    # 创建 preferences 表
    op.create_table('preferences',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('world_id', sa.String(length=50), nullable=True),
        sa.Column('story_id', sa.UUID(), nullable=True),
        sa.Column('tag', sa.String(length=50), nullable=False),
        sa.Column('weight', sa.Float(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['story_id'], ['stories.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_preference_user_tag', 'preferences', ['user_id', 'tag'], unique=False)
    op.create_index('idx_preference_user_world', 'preferences', ['user_id', 'world_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # 删除 preferences 表
    op.drop_index('idx_preference_user_world', table_name='preferences')
    op.drop_index('idx_preference_user_tag', table_name='preferences')
    op.drop_table('preferences')
    
    # 删除列
    op.drop_column('turns', 'preference_tags')
    op.drop_column('stories', 'status')
    
    # 删除枚举类型
    op.execute("DROP TYPE storystatus")