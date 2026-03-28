"""
世界观 API - 获取可用世界观列表
"""

from fastapi import APIRouter
from app.templates.manager import template_manager
from fastapi import APIRouter, HTTPException

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


@router.get("/{world_id}/templates")
async def get_world_templates(world_id: str):
    """获取指定世界观的角色模板"""
    templates = template_manager.get_templates(world_id)
    return {
        "world": world_id,
        "templates": templates
    }


@router.get("/{world_id}/templates/random")
async def get_random_template(world_id: str):
    """随机获取一个角色模板"""
    import random
    templates = template_manager.get_templates(world_id)
    if not templates:
        return {"world": world_id, "template": None}
    
    template = random.choice(templates)
    return {
        "world": world_id,
        "template": template
    }

@router.get("/tags")
async def get_all_tags():
    """获取所有可用标签"""
    tags = template_manager.get_all_tags()
    return {"tags": tags}


@router.get("/{world_id}/templates/by-tag/{tag}")
async def get_templates_by_tag(world_id: str, tag: str):
    """根据标签获取指定世界观的模板"""
    templates = template_manager.get_templates_by_tag(tag, world_id)
    return {
        "world": world_id,
        "tag": tag,
        "templates": [t["template"] for t in templates]
    }


@router.post("/recommend")
async def recommend_templates(request: dict):
    """根据偏好标签推荐模板"""
    preferred_tags = request.get("preferred_tags", [])
    world_id = request.get("world_id")
    limit = request.get("limit", 3)
    
    recommendations = template_manager.recommend_by_tags(preferred_tags, world_id, limit)
    return {
        "preferred_tags": preferred_tags,
        "recommendations": recommendations
    }

@router.post("/generate-template")
async def generate_template(request: dict):
    """AI 动态生成角色模板"""
    world_id = request.get("world_id")
    tags = request.get("tags", [])
    
    if not world_id or not tags:
        raise HTTPException(status_code=400, detail="需要提供 world_id 和 tags")
    
    template = await template_manager.generate_template_by_ai(world_id, tags)
    
    if not template:
        raise HTTPException(status_code=500, detail="AI 生成模板失败")
    
    return template