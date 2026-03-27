"""
赛博朋克世界观 - 角色模板
"""

TEMPLATES = [
    {
        "id": "cyber_hacker",
        "name": "网络黑客",
        "description": "穿梭于数据洪流中的幽灵，任何系统都有漏洞。",
        "opening": "我的义体手臂在键盘上敲出最后一串代码，防火墙上撕开一道口子。巨型企业的秘密，从来就不该是秘密。",
        "tags": ["黑客", "反抗", "数字幽灵"]
    },
    {
        "id": "cyber_ripperdoc",
        "name": "义体医生",
        "description": "在黑市为底层人安装义体的地下医生。",
        "opening": "手术台上躺着今晚的第三个病人，他的脊椎被改装过，里面藏着我不想知道的秘密。",
        "tags": ["医生", "黑市", "秘密"]
    },
    {
        "id": "cyber_mercenary",
        "name": "雇佣兵",
        "description": "拿钱办事的街头佣兵，在这个城市里活着就是最大的胜利。",
        "opening": "信用点到账，目标资料显示在屏幕上。又一个要死的企业中层。我检查枪械，走出公寓——今晚的霓虹格外刺眼。",
        "tags": ["佣兵", "暴力", "生存"]
    },
    {
        "id": "cyber_corpo",
        "name": "企业叛逃者",
        "description": "曾经是巨型企业的中层，因为知道太多而被追杀。",
        "opening": "他们抹去了我所有的档案，但我还活着。硬盘里的数据，足够让整个董事会进监狱。",
        "tags": ["叛逃", "复仇", "情报"]
    }
]


def get_templates():
    return TEMPLATES


def get_template_by_id(template_id: str):
    for t in TEMPLATES:
        if t["id"] == template_id:
            return t
    return None