"""
都市传说世界观 - 角色模板
"""

TEMPLATES = [
    {
        "id": "urban_blogger",
        "name": "怪谈博主",
        "description": "专门收集都市传说的自媒体博主，以为只是故事。",
        "opening": "粉丝私信里提到青石巷的红伞女，我以为只是又一个都市传说，直到我家门口真的出现了一把红伞。",
        "tags": ["博主", "调查", "卷入"]
    },
    {
        "id": "urban_scholar",
        "name": "民俗学者",
        "description": "研究民间禁忌的学者，从书斋走向现实。",
        "opening": "我在旧书摊上买到一本手抄本，里面记载的禁忌仪式，与最近失踪案的细节惊人地相似。",
        "tags": ["学者", "禁忌", "真相"]
    },
    {
        "id": "urban_police",
        "name": "深夜巡警",
        "description": "夜班巡逻的警察，见过城市的另一面。",
        "opening": "凌晨三点的报警电话，废弃医院三楼有灯光。我去了，不该去的。",
        "tags": ["警察", "巡逻", "规则"]
    },
    {
        "id": "urban_taxi",
        "name": "夜班司机",
        "description": "开夜班出租车的司机，接过的客人里有一些不是人。",
        "opening": "那个乘客上车后只说了一个地址：老城区第四人民医院。那地方十年前就关了。后视镜里，后座是空的。",
        "tags": ["司机", "见证者", "幸存"]
    }
]


def get_templates():
    return TEMPLATES


def get_template_by_id(template_id: str):
    for t in TEMPLATES:
        if t["id"] == template_id:
            return t
    return None