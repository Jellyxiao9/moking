"""
克苏鲁神话世界观 - 角色模板
"""

TEMPLATES = [
    {
        "id": "cthulhu_professor",
        "name": "大学教授",
        "description": "米斯卡托尼克大学的人类学教授，研究古籍时发现了不该发现的东西。",
        "opening": "图书馆的旧书堆里，我找到了一本用人类皮肤装订的典籍。翻开第一页，我就知道自己不该看。",
        "tags": ["学者", "禁忌知识", "理智"]
    },
    {
        "id": "cthulhu_detective",
        "name": "私家侦探",
        "description": "受雇调查失踪案，却发现了超越人智的真相。",
        "opening": "雇主说他的女儿加入了阿卡姆的一个秘密社团。我跟踪了几周，发现那个社团崇拜的东西，不属于这个世界。",
        "tags": ["侦探", "调查", "不可名状"]
    },
    {
        "id": "cthulhu_journalist",
        "name": "报社记者",
        "description": "调查小镇集体失踪案，揭开不可名状的真相。",
        "opening": "印斯茅斯的居民在一夜之间全部消失。我在镇公所的档案室里，找到了一本用古怪文字写成的日记。",
        "tags": ["记者", "真相", "疯狂"]
    },
    {
        "id": "cthulhu_artist",
        "name": "落魄画家",
        "description": "患有失眠症的画家，画出来的东西不该存在于世上。",
        "opening": "我画了一整夜，醒来时画布上是一幅我不记得画过的画。画里的城市，在现实中有原型。",
        "tags": ["艺术家", "梦境", "侵蚀"]
    }
]


def get_templates():
    return TEMPLATES


def get_template_by_id(template_id: str):
    for t in TEMPLATES:
        if t["id"] == template_id:
            return t
    return None