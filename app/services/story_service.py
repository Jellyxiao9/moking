"""
故事服务 - 编排剧情生成流程
"""

from uuid import UUID
from app.engine.narrator import Narrator
from app.engine.choice_parser import extract_choices
from app.repositories.story_repo import StoryRepo
from app.repositories.turn_repo import TurnRepo


class StoryService:
    """故事服务：协调叙事引擎和仓储"""

    def __init__(self):
        self.narrator = Narrator()
        self.story_repo = StoryRepo()
        self.turn_repo = TurnRepo()

    def start_story(
        self,
        world: str,
        opening: str,
        title: str = None
    ) -> dict:
        """
        开始一个新故事

        Args:
            world: 世界观 (cyberpunk/fantasy/noir)
            opening: 玩家的开场描述
            title: 故事标题（可选）

        Returns:
            {
                "story_id": 故事ID,
                "content": 生成的剧情,
                "choices": ["选项1", "选项2", "选项3"]
            }
        """
        # 1. 生成开场剧情
        story_content = self.narrator.generate(
            world=world,
            scene_description=opening,
            history=None
        )

        # 2. 提取选项
        choices = extract_choices(story_content)

        # 3. 创建故事记录
        if not title:
            title = f"{world} 冒险 - {opening[:30]}"
        story = self.story_repo.create(
            title=title,
            world=world
        )

        # 4. 保存第一轮对话
        self.turn_repo.create(
            story_id=story.id,
            turn_number=1,
            narrative=story_content,
            choices=choices
        )

        return {
            "story_id": str(story.id),
            "content": story_content,
            "choices": choices
        }

    def continue_story(
        self,
        story_id: UUID,
        user_choice: str
    ) -> dict:
        """
        继续故事

        Args:
            story_id: 故事ID
            user_choice: 玩家选择的选项

        Returns:
            {
                "content": 生成的剧情,
                "choices": ["选项1", "选项2", "选项3"],
                "turn_number": 当前轮次
            }
        """
        # 1. 获取故事信息
        story = self.story_repo.get_by_id(story_id)
        if not story:
            raise ValueError(f"故事不存在: {story_id}")

        # 2. 获取历史记录
        history = self.turn_repo.get_history(story_id)

        # 3. 获取当前轮次
        last_turn = self.turn_repo.get_last_turn(story_id)
        next_turn_number = (last_turn.turn_number + 1) if last_turn else 1

        # 4. 生成下一段剧情
        story_content = self.narrator.generate(
            world=story.world.value,  # 枚举转字符串
            scene_description=user_choice,
            history=history
        )

        # 5. 提取选项
        choices = extract_choices(story_content)

        # 6. 保存新的一轮
        turn = self.turn_repo.create(
            story_id=story_id,
            turn_number=next_turn_number,
            narrative=story_content,
            choices=choices,
            user_choice=user_choice
        )

        # 7. 更新故事摘要（用最新剧情的前100字作为摘要）
        self.story_repo.update_summary(story_id, story_content[:100])

        return {
            "content": story_content,
            "choices": choices,
            "turn_number": turn.turn_number
        }