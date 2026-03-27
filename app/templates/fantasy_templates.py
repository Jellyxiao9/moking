"""
奇幻世界观 - 角色模板
"""

TEMPLATES = [
    {
        "id": "fantasy_swordsman",
        "name": "流浪剑客",
        "description": "四海为家的剑士，剑下亡魂比朋友多。",
        "opening": "酒馆的门被风推开，我握紧剑柄。角落里坐着一个人，他说知道哪里有我要找的东西。",
        "tags": ["剑士", "流浪", "战斗"]
    },
    {
        "id": "fantasy_mage",
        "name": "学院法师",
        "description": "从魔法学院毕业的年轻法师，理论丰富，实战为零。",
        "opening": "魔法学院的毕业证书还带着墨香，但学费已经花光了我所有的金币。听说冒险者公会在招人。",
        "tags": ["法师", "菜鸟", "成长"]
    },
    {
        "id": "fantasy_ranger",
        "name": "精灵游侠",
        "description": "来自古老森林的精灵，弓术精准，不愿与人类多言。",
        "opening": "人类的城市让我不适，但族长的命令让我必须找到那把被盗的精灵弓。",
        "tags": ["精灵", "游侠", "弓箭"]
    },
    {
        "id": "fantasy_cleric",
        "name": "圣殿牧师",
        "description": "侍奉神明的牧师，信仰是他唯一的武器。",
        "opening": "神殿的钟声在远处响起，而我站在黑暗的街道上。神明说要有光，但这里只有我手中的圣光。",
        "tags": ["牧师", "信仰", "治愈"]
    }
]


def get_templates():
    return TEMPLATES


def get_template_by_id(template_id: str):
    for t in TEMPLATES:
        if t["id"] == template_id:
            return t
    return None