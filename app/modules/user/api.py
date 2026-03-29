"""
用户 API - 登录、注册、个人主页
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from uuid import UUID
from app.modules.user.services.auth_service import AuthService
from app.modules.user.services.user_service import UserService

router = APIRouter(prefix="/user", tags=["user"])
auth_service = AuthService()
user_service = UserService()


class RegisterRequest(BaseModel):
    phone: str
    password: str
    nickname: str = "旅行者"


class LoginRequest(BaseModel):
    phone: str
    password: str


class GuestLoginResponse(BaseModel):
    user_id: str
    is_guest: bool
    message: str


class UserProfileResponse(BaseModel):
    user_id: str
    nickname: str
    avatar: str
    is_guest: bool
    story_count: int
    favorite_tags: list


@router.post("/register")
async def register(request: RegisterRequest):
    """手机号注册"""
    result = auth_service.register(
        phone=request.phone,
        password=request.password,
        nickname=request.nickname
    )
    if not result:
        raise HTTPException(status_code=400, detail="注册失败，手机号可能已存在")
    return result


@router.post("/login")
async def login(request: LoginRequest):
    """手机号登录"""
    result = auth_service.login(
        phone=request.phone,
        password=request.password
    )
    if not result:
        raise HTTPException(status_code=401, detail="手机号或密码错误")
    return result


@router.post("/guest", response_model=GuestLoginResponse)
async def guest_login():
    """游客登录"""
    user_id = auth_service.create_guest()
    return {
        "user_id": str(user_id),
        "is_guest": True,
        "message": "游客登录成功，注册后可保存数据"
    }


@router.get("/profile/{user_id}", response_model=UserProfileResponse)
async def get_profile(user_id: str):
    """获取用户主页信息"""
    profile = user_service.get_profile(UUID(user_id))
    if not profile:
        raise HTTPException(status_code=404, detail="用户不存在")
    return profile


@router.put("/profile/{user_id}")
async def update_profile(user_id: str, nickname: str = None, avatar: str = None):
    """更新用户信息"""
    result = user_service.update_profile(UUID(user_id), nickname, avatar)
    if not result:
        raise HTTPException(status_code=400, detail="更新失败")
    return {"message": "更新成功"}


@router.get("/{user_id}/stories")
async def get_user_stories(user_id: str):
    """获取用户的所有故事"""
    stories = user_service.get_user_stories(UUID(user_id))
    return {"stories": stories}