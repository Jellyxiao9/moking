"""
古风权谋世界观 - 角色模板
"""

TEMPLATES = [
    {
        "id": "strategy_scholar",
        "name": "寒门进士",
        "description": "十年寒窗，一朝中第，却发现朝堂比考场凶险百倍。",
        "opening": "翰林院的清茶还没凉透，我就被卷入了一场弹劾案。首辅大人的眼神，比考场上的考官更让人心寒。",
        "tags": ["文官", "清流", "仕途"]
    },
    {
        "id": "strategy_guard",
        "name": "锦衣卫",
        "description": "天子亲军，锦衣夜行。手中刀快，心中事重。",
        "opening": "密令上是三个字：查。线索指向的是一座王府，我握刀的手在袖中微微发颤。",
        "tags": ["密探", "忠诚", "抉择"]
    },
    {
        "id": "strategy_adviser",
        "name": "王府幕僚",
        "description": "寄身王府，为主分忧。棋盘上的每一颗棋子，都是一条人命。",
        "opening": "王爷把一杯酒推到我面前，说：先生，是时候让那些人知道，谁是京城真正的主人。",
        "tags": ["谋士", "权谋", "算计"]
    },
    {
        "id": "strategy_princess",
        "name": "和亲公主",
        "description": "远嫁他国的公主，在异乡的宫廷中求存。",
        "opening": "嫁衣如火，凤冠沉重。我踏出宫门的那一刻，身后的繁华就成了再也回不去的故乡。",
        "tags": ["公主", "和亲", "隐忍"]
    }
]


def get_templates():
    return TEMPLATES


def get_template_by_id(template_id: str):
    for t in TEMPLATES:
        if t["id"] == template_id:
            return t
    return None