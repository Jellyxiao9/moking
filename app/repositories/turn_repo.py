"""
对话轮次仓储层 - 管理每轮对话的数据库操作
"""

from sqlalchemy.orm import Session
from uuid import UUID
import json
from app.infrastructure.database import get_db
from app.models.turn import Turn


class TurnRepo:
    """对话轮次仓储"""

    def __init__(self, db: Session = None):
        self.db = db or next(get_db())

    def create(
        self,
        story_id: UUID,
        turn_number: int,
        narrative: str,
        choices: list[str] = None,
        user_choice: str = None
    ) -> Turn:
        """创建新的对话轮次"""
        turn = Turn(
            story_id=story_id,
            turn_number=turn_number,
            narrative=narrative,
            choices=json.dumps(choices, ensure_ascii=False) if choices else None,
            user_choice=user_choice
        )
        self.db.add(turn)
        self.db.commit()
        self.db.refresh(turn)
        return turn

    def get_by_story(self, story_id: UUID) -> list[Turn]:
        """获取故事的所有对话轮次"""
        return self.db.query(Turn).filter(
            Turn.story_id == story_id
        ).order_by(Turn.turn_number).all()

    def get_history(self, story_id: UUID, max_turns: int = 10) -> list[dict]:
        """
        获取历史记录（用于 LLM 上下文）
        返回格式: [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
        """
        turns = self.get_by_story(story_id)
        history = []
        for turn in turns[-max_turns:]:
            # user_choice 是用户的选择
            if turn.user_choice:
                history.append({"role": "user", "content": turn.user_choice})
            history.append({"role": "assistant", "content": turn.narrative})
        return history

    def get_last_turn(self, story_id: UUID) -> Turn | None:
        """获取最后一轮对话"""
        return self.db.query(Turn).filter(
            Turn.story_id == story_id
        ).order_by(Turn.turn_number.desc()).first()