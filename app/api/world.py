"""
世界观 API - 获取可用世界观列表
"""

from fastapi import APIRouter

router = APIRouter(prefix="/world", tags=["world"])


@router.get("/list")
async def list_worlds():
    """获取所有可用的世界观"""
    worlds = [
        {"id": "noir", "name": "黑色电影", "description": "1952年，永远下雨的罪恶都市"},
        {"id": "cyberpunk", "name": "赛博朋克", "description": "2077年，霓虹灯下的高科技低生活"},
        {"id": "fantasy", "name": "奇幻", "description": "剑与魔法的中世纪世界"},
        {"id": "xianxia", "name": "东方玄幻", "description": "九天玄界，灵气复苏，修仙问道"},
        {"id": "strategy", "name": "古风权谋", "description": "天盛王朝，朝堂博弈，人心难测"},
        {"id": "urban", "name": "都市传说", "description": "雾都怪谈，午夜禁忌，规则求生"},
        {"id": "cthulhu", "name": "克苏鲁神话", "description": "1920年代，不可名状的古老恐惧"},
        {"id": "wasteland", "name": "废土生存", "description": "2087年，核战后的末世废土"}
    ]
    return {"worlds": worlds}