"""
故事服务 - 编排剧情生成流程
"""

from uuid import UUID
import re
from app.engine.narrator import Narrator
from app.engine.choice_parser import extract_choices
from app.repositories.story_repo import StoryRepo
from app.repositories.turn_repo import TurnRepo
from app.modules.preference import PreferenceRecorder


def extract_tags_from_text(text: str) -> list:
    """从文本中提取标签（简单关键词匹配）"""
    # 常见标签关键词
    tag_keywords = {
        "调查": ["调查", "查", "找", "线索", "证据"],
        "战斗": ["战斗", "打", "攻击", "对抗"],
        "交涉": ["交涉", "谈判", "说服", "劝说"],
        "探索": ["探索", "查看", "观察", "检查"],
        "潜行": ["潜行", "偷偷", "悄悄", "隐藏"],
        "科技": ["科技", "黑客", "网络", "义体"],
        "魔法": ["魔法", "咒语", "法术", "灵力"],
        "修仙": ["修仙", "修炼", "灵气", "筑基"],
        "权谋": ["权谋", "朝堂", "谋略", "算计"],
        "怪谈": ["怪谈", "传说", "禁忌", "灵异"],
        "理智": ["理智", "疯狂", "恐惧", "精神"],
        "生存": ["生存", "物资", "辐射", "废土"],
    }
    
    tags = []
    text_lower = text.lower()
    for tag, keywords in tag_keywords.items():
        for kw in keywords:
            if kw in text:
                tags.append(tag)
                break
    return tags


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

        # 3. 自动生成标题（如果未提供）
        if not title:
            try:
                title_prompt = f"根据以下故事开场，生成一个简短的标题（10字以内，不要加引号，不要加标点）：\n{opening}"
                response = self.narrator.client.chat.completions.create(
                    model=self.narrator.model,
                    messages=[{"role": "user", "content": title_prompt}],
                    max_tokens=20,
                    temperature=0.7
                )
                title = response.choices[0].message.content.strip()
                # 清理标题：去掉引号和多余符号
                title = title.strip('"').strip("'").strip()
                if len(title) > 20 or not title:
                    title = f"{world} 冒险"
            except:
                title = f"{world} 冒险"

        # 4. 创建故事记录
        story = self.story_repo.create(
            title=title,
            world=world
        )

        # 5. 保存第一轮对话
        self.turn_repo.create(
            story_id=story.id,
            turn_number=1,
            narrative=story_content,
            choices=choices
        )

        # 6. 记录偏好（开场第一轮，暂时不记录，等后续有用户ID再完善）
        # 注意：第一轮时 story.user_id 可能为空，等用户系统完善后添加

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

        # 8. 记录偏好
        try:
            pref_recorder = PreferenceRecorder()
            
            # 从用户选择中提取标签
            tags = extract_tags_from_text(user_choice)
            
            # 如果有用户 ID，记录偏好
            if story.user_id:
                pref_recorder.record(
                    user_id=str(story.user_id),
                    world_id=story.world.value,
                    story_id=str(story_id),
                    tags=tags
                )
            # 游客模式暂不记录，等游客系统完善后再添加
                
        except Exception as e:
            print(f"记录偏好失败: {e}")

        return {
            "content": story_content,
            "choices": choices,
            "turn_number": turn.turn_number
        }