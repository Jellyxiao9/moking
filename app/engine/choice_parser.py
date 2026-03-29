"""
选项解析器 - 从剧情文本中提取结构化的选项
"""

import re


def extract_choices(story_text: str, num_choices: int = 3, narrator=None) -> list:
    """
    从剧情文本中提取选项

    Args:
        story_text: 生成的剧情文本
        num_choices: 期望的选项数量（默认3个）
        narrator: 可选，用于 AI 生成选项（备用）

    Returns:
        选项列表
    """
    # 查找 "你可以：" 后面的选项
    patterns = [
        r'你可以[：:]\s*\n?((?:\d+\.\s*[^\n]+\n?)+)',  # 你可以：1. xxx 2. xxx
        r'接下来[：:]\s*\n?((?:\d+\.\s*[^\n]+\n?)+)',  # 接下来：1. xxx
        r'选项[：:]\s*\n?((?:\d+\.\s*[^\n]+\n?)+)',    # 选项：1. xxx
        r'(?:\d+\.\s*[^\n]+)(?:\n\d+\.\s*[^\n]+)+',   # 直接匹配数字列表
    ]
    
    choices = []
    for pattern in patterns:
        match = re.search(pattern, story_text, re.MULTILINE)
        if match:
            # 提取数字列表
            list_text = match.group(1) if match.lastindex else match.group(0)
            nums = re.findall(r'\d+\.\s*([^\n]+)', list_text)
            if nums:
                choices = [c.strip() for c in nums]
                break
    
    # 清理选项
    choices = [c.strip() for c in choices if c.strip()]
    
    # 如果找到足够的选项，返回
    if len(choices) >= num_choices:
        return choices[:num_choices]
    
    # 如果没找到，用启发式方法
    if not choices:
        choices = _extract_by_heuristic(story_text, num_choices)
    
    # 最后保底：调用 AI 生成（如果提供了 narrator）
    if len(choices) < num_choices and narrator:
        ai_choices = _generate_choices_by_ai(story_text, num_choices, narrator)
        if ai_choices:
            return ai_choices[:num_choices]
    
    # 保底默认选项（但尽量不用）
    if len(choices) < num_choices:
        defaults = _get_default_choices()
        choices.extend(defaults[:num_choices - len(choices)])
    
    return choices[:num_choices]


def _generate_choices_by_ai(story_text: str, num_choices: int, narrator) -> list:
    """调用 AI 生成选项（备用方案）"""
    prompt = f"""根据以下剧情，生成 {num_choices} 个合理的下一步行动选项。

剧情：
{story_text}

要求：
1. 选项要符合剧情逻辑
2. 每个选项要具体、有行动性
3. 不要使用"继续前进"这种泛泛的选项
4. 直接返回选项列表，每行一个，用数字编号

示例格式：
1. 跟进那个神秘人
2. 仔细检查信封里的照片
3. 去锦绣大道17号看看

请直接返回选项："""

    try:
        response = narrator.client.chat.completions.create(
            model=narrator.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.8
        )
        
        content = response.choices[0].message.content
        choices = []
        for line in content.strip().split('\n'):
            match = re.match(r'^\d+\.\s*(.+)$', line.strip())
            if match:
                choices.append(match.group(1))
        
        return choices[:num_choices]
    except Exception as e:
        print(f"AI 生成选项失败: {e}")
        return []


def _extract_by_heuristic(story_text: str, num_choices: int) -> list:
    """启发式提取：寻找包含动作关键词的句子"""
    action_keywords = ['可以', '也许', '不妨', '试试', '要么', '或者', '是...还是']
    
    sentences = re.split(r'[。！？]', story_text)
    candidates = []
    for sent in sentences:
        sent = sent.strip()
        if not sent:
            continue
        if any(kw in sent for kw in action_keywords):
            cleaned = re.sub(r'^(你|你可以|也许你|不妨|试试|要么|或者)', '', sent)
            candidates.append(cleaned[:60])
    
    seen = set()
    unique_candidates = []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            unique_candidates.append(c)
    
    return unique_candidates[:num_choices]


def _get_default_choices() -> list:
    """保底默认选项（尽量少用）"""
    return [
        "继续前进",
        "仔细观察周围",
        "和其他人交谈",
    ]