"""
叙事引擎 - 核心剧情生成器
负责组装 prompt，调用 LLM 生成故事内容
"""

from app.infrastructure.llm_client import get_llm_client
from app.engine.consistency_rag import get_context


class Narrator:
    """叙事者：负责生成故事剧情"""

    def __init__(self):
        self.client = get_llm_client()
        self.model = "deepseek-chat"

    def generate(
        self,
        world: str,
        scene_description: str,
        history: list = None,
        preferences: list = None,
        max_tokens: int = 800,
    ) -> str:
        """
        生成剧情

        Args:
            world: 世界观名称 (cyberpunk/fantasy/noir)
            scene_description: 当前场景描述（玩家输入或开场白）
            history: 之前的对话历史（可选）
            preferences: 用户偏好标签列表（可选）
            max_tokens: 最大生成 token 数

        Returns:
            生成的剧情文本
        """
        # 1. 检索相关世界观片段
        context = get_context(world, scene_description)

        # 2. 构建 system prompt（传入 preferences）
        system_prompt = self._build_system_prompt(world, context, preferences)

        # 3. 构建用户消息
        user_prompt = self._build_user_prompt(scene_description, history)

        # 4. 调用 LLM
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=max_tokens,
            temperature=0.8,
        )

        return response.choices[0].message.content

    def _build_system_prompt(self, world: str, context: str, preferences: list = None) -> str:
        """构建系统提示词（包含世界观）"""
        base_prompt = f"""你是一个专业的互动叙事游戏主持人（DM），正在为玩家主持一场以「{world}」世界观为背景的文字冒险游戏。

## 你的核心职责
1. **保持世界观一致性**：严格遵循下面的世界观设定，不能前后矛盾
2. **生动的场景描写**：用细腻的文字描绘场景、氛围、人物神态
3. **推进剧情**：每次回复推动故事向前发展，不要原地打转
4. **控制节奏**：每段回复 150-300 字左右，给玩家留下选择空间

## 世界观设定
{context}

## 回复格式要求
1. 直接输出剧情内容，不要加「剧情：」这类前缀
2. 剧情结束后，留出 2-3 个自然的选择方向，但不要显式列出选项（选项由另一个模块单独提取）
3. 使用第二人称「你」来指代玩家
4. 语言风格：中文，文学性强，有沉浸感

记住：你是主持人，不是玩家。你的任务是创造世界，让玩家在这个世界中做出选择。"""
        return base_prompt

    def _build_user_prompt(self, scene_description: str, history: list = None) -> str:
        """构建用户提示词"""
        if not history:
            # 开场：玩家描述初始场景或角色
            return f"""请根据以下玩家开场，开始这个故事：

玩家：{scene_description}

请生成第一段剧情。"""

        # 后续轮次：包含历史 + 当前选择
        history_text = self._format_history(history)
        return f"""## 之前的剧情
{history_text}

## 玩家现在的行动
{scene_description}

请根据玩家行动，生成接下来的剧情。"""

    def _format_history(self, history: list) -> str:
        """格式化历史记录"""
        formatted = []
        for turn in history[-6:]:  # 只保留最近6轮，避免超 token
            if turn.get("role") == "user":
                formatted.append(f"玩家：{turn.get('content', '')}")
            else:
                formatted.append(f"剧情：{turn.get('content', '')}")
        return "\n\n".join(formatted)