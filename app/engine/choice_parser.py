"""
选项解析器 - 从剧情文本中提取结构化的选项
"""

import re


def extract_choices(story_text: str, num_choices: int = 3) -> list:
    """
    从剧情文本中提取选项

    Args:
        story_text: 生成的剧情文本
        num_choices: 期望的选项数量（默认3个）

    Returns:
        选项列表，例如 ["去码头调查", "回警局查档案", "找线人打听消息"]
    """
    # 方法1：查找显式的选项标记
    # 匹配格式：1. xxx / 2. xxx / - xxx / * xxx
    patterns = [
        r'(?:\d+\.\s*)([^\n]+)',           # 1. 选项内容
        r'(?:-\s*)([^\n]+)',                # - 选项内容
        r'(?:\*\s*)([^\n]+)',               # * 选项内容
        r'选项[：:]\s*([^\n]+)',            # 选项：内容
    ]

    choices = []
    for pattern in patterns:
        matches = re.findall(pattern, story_text)
        if matches:
            choices.extend(matches[:num_choices])
            break

    # 方法2：如果没找到显式标记，用启发式方法
    if not choices:
        choices = _extract_by_heuristic(story_text, num_choices)

    # 清理选项：去除首尾空格，过滤空字符串
    choices = [c.strip() for c in choices if c.strip()]

    # 确保返回恰好 num_choices 个选项
    if len(choices) < num_choices:
        # 补充默认选项
        defaults = _get_default_choices()
        choices.extend(defaults[:num_choices - len(choices)])

    return choices[:num_choices]


def _extract_by_heuristic(story_text: str, num_choices: int) -> list:
    """
    启发式提取：寻找包含动作关键词的句子
    """
    # 常见的动作关键词
    action_keywords = ['可以', '也许', '不妨', '试试', '要么', '或者', '是...还是']

    # 按句号分割
    sentences = re.split(r'[。！？]', story_text)

    candidates = []
    for sent in sentences:
        sent = sent.strip()
        if not sent:
            continue
        # 检查是否包含动作关键词
        if any(kw in sent for kw in action_keywords):
            # 清理句子，提取核心动作
            cleaned = re.sub(r'^(你|你可以|也许你|不妨|试试|要么|或者)', '', sent)
            candidates.append(cleaned[:50])  # 限制长度

    # 去重
    seen = set()
    unique_candidates = []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            unique_candidates.append(c)

    return unique_candidates[:num_choices]


def _get_default_choices() -> list:
    """
    通用默认选项
    """
    return [
        "继续前进",
        "仔细观察周围",
        "和其他人交谈",
        "暂时离开",
        "回忆相关信息",
    ]