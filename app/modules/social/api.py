"""
社交分享 API
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from app.modules.social.services.social_service import SocialService

router = APIRouter(prefix="/social", tags=["social"])
service = SocialService()


class ShareRequest(BaseModel):
    story_id: str
    user_id: str
    share_type: str = "ending"


class ShareResponse(BaseModel):
    share_id: str
    share_url: str
    created_at: datetime


@router.post("/share", response_model=ShareResponse)
async def create_share(request: ShareRequest):
    """创建分享"""
    share = service.create_share(
        story_id=UUID(request.story_id),
        user_id=UUID(request.user_id),
        share_type=request.share_type
    )
    if not share:
        raise HTTPException(status_code=400, detail="分享失败")
    return share


@router.get("/share/{share_id}")
async def get_share(share_id: str):
    """获取分享内容"""
    share = service.get_share(UUID(share_id))
    if not share:
        raise HTTPException(status_code=404, detail="分享不存在")
    return share


@router.get("/user/{user_id}/shares")
async def get_user_shares(user_id: str):
    """获取用户的所有分享"""
    shares = service.get_user_shares(UUID(user_id))
    return {"shares": shares}


@router.post("/share/{share_id}/view")
async def increment_view_count(share_id: str):
    """增加浏览次数"""
    service.increment_view_count(UUID(share_id))
    return {"message": "ok"}