"""
东方玄幻世界观 - 角色模板
"""

TEMPLATES = [
    {
        "id": "xianxia_sanxiu",
        "name": "散修",
        "description": "无门无派的散修，靠自己摸索修行之道。",
        "opening": "我在灵气稀薄的荒山修炼了十年，终于筑基。听说九天玄宗在招收外门弟子，这是我唯一的机会。",
        "tags": ["散修", "奋斗", "草根"]
    },
    {
        "id": "xianxia_disciples",
        "name": "宗门弟子",
        "description": "大宗门的内门弟子，资质上佳，但还没经历过真正的历练。",
        "opening": "师父让我下山历练，说是修道之人须经红尘。第一站，便是传说中有妖兽出没的青云山脉。",
        "tags": ["宗门", "历练", "成长"]
    },
    {
        "id": "xianxia_yaozu",
        "name": "妖族后裔",
        "description": "身负妖族血脉，在人类修士的世界里隐藏身份。",
        "opening": "我的血脉是秘密，也是诅咒。但最近出现的妖兽骚乱，让我不得不使用那些不该用的力量。",
        "tags": ["妖族", "隐藏", "身份危机"]
    }
]


def get_templates():
    return TEMPLATES


def get_template_by_id(template_id: str):
    for t in TEMPLATES:
        if t["id"] == template_id:
            return t
    return None