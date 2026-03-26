"""
世界观 API - 获取可用世界观列表
"""

from fastapi import APIRouter
from app.models.story import WorldType

router = APIRouter(prefix="/world", tags=["world"])


@router.get("/list")
async def list_worlds():
    """获取所有可用的世界观"""
    worlds = [
        {"id": "cyberpunk", "name": "赛博朋克", "description": "2077年，霓虹灯下的高科技低生活"},
        {"id": "fantasy", "name": "奇幻", "description": "剑与魔法的中世纪世界"},
        {"id": "noir", "name": "黑色电影", "description": "1952年，永远下雨的罪恶都市"}
    ]
    return {"worlds": worlds}