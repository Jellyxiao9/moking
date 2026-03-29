"""
FastAPI 主入口
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from app.api import story, world
from fastapi.staticfiles import StaticFiles
from app.modules.user.api import router as user_router
from app.modules.social.api import router as social_router

app = FastAPI(
    title="墨境 Storycraft",
    description="AI 驱动的动态互动小说引擎",
    version="1.0.0"
)

# 允许跨域（前端开发用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录（前端）
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/frontend", StaticFiles(directory=frontend_path, html=True), name="frontend")

@app.get("/")
async def root():
    return {"message": "墨境 Storycraft API 运行中", "status": "ok"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


# 注册路由
app.include_router(world.router)
app.include_router(story.router)
app.include_router(user_router)
app.include_router(social_router)