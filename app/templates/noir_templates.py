"""
黑色电影世界观 - 角色模板
"""

TEMPLATES = [
    {
        "id": "noir_detective",
        "name": "私家侦探",
        "description": "独自经营事务所的侦探，见过太多人性的黑暗面。",
        "opening": "我是一家小侦探事务所的老板，今天收到一封匿名信，约我在雨夜的码头见面。",
        "tags": ["调查", "硬汉", "孤独"]
    },
    {
        "id": "noir_journalist",
        "name": "报社记者",
        "description": "追逐真相的记者，相信文字可以改变世界。",
        "opening": "我是《城市纪事报》的记者，正在调查一起市长牵涉的腐败案，有人开始威胁我收手。",
        "tags": ["调查", "正义", "危险"]
    },
    {
        "id": "noir_ex_cop",
        "name": "退役警探",
        "description": "因不肯同流合污而被踢出警局的前警探。",
        "opening": "三个月前我还是警局的探长，现在只是雨夜城里一个喝酒等死的废人，直到那个女人推开了我的门。",
        "tags": ["复仇", "堕落", "救赎"]
    }
]


def get_templates():
    return TEMPLATES


def get_template_by_id(template_id: str):
    for t in TEMPLATES:
        if t["id"] == template_id:
            return t
    return None