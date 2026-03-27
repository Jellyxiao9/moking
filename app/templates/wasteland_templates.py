"""
废土生存世界观 - 角色模板
"""

TEMPLATES = [
    {
        "id": "wasteland_scavenger",
        "name": "拾荒者",
        "description": "在废墟中翻找物资的流浪者，知道哪里可能有水、哪里有危险。",
        "opening": "我在旧城的废墟里翻了一整天，只找到半盒过期的罐头和几颗子弹。远处传来掠夺者的引擎声。",
        "tags": ["拾荒", "生存", "警觉"]
    },
    {
        "id": "wasteland_vault",
        "name": "避难所居民",
        "description": "从地下避难所走出来的人，对废土一无所知。",
        "opening": "三十四年了，门终于打开。外面的天空是黄色的，空气里有铁锈的味道。我应该回去的，但我没有。",
        "tags": ["新人", "天真", "适应"]
    },
    {
        "id": "wasteland_guard",
        "name": "商队护卫",
        "description": "用枪法换口粮的雇佣兵，见过废土上的一切。",
        "opening": "这趟活是护送一批水去大集市。路上有七个人盯着我们的货，我会在三天内杀掉他们，或者被他们杀掉。",
        "tags": ["雇佣兵", "枪法", "冷酷"]
    },
    {
        "id": "wasteland_scientist",
        "name": "前科学家",
        "description": "战前的研究员，在废土上寻找重建文明的方法。",
        "opening": "实验室的废墟里还有未损坏的设备。我的研究能救活这片土地，前提是我能活着走出辐射区。",
        "tags": ["科学家", "希望", "脆弱"]
    }
]


def get_templates():
    return TEMPLATES


def get_template_by_id(template_id: str):
    for t in TEMPLATES:
        if t["id"] == template_id:
            return t
    return None