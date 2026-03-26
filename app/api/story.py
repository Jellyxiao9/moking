"""
故事 API - 开始和继续故事
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from uuid import UUID
from app.services.story_service import StoryService

router = APIRouter(prefix="/story", tags=["story"])
service = StoryService()


class StartStoryRequest(BaseModel):
    world: str
    opening: str
    title: str | None = None


class StartStoryResponse(BaseModel):
    story_id: str
    content: str
    choices: list[str]


class ContinueStoryRequest(BaseModel):
    story_id: str
    user_choice: str


class ContinueStoryResponse(BaseModel):
    content: str
    choices: list[str]
    turn_number: int


@router.post("/start", response_model=StartStoryResponse)
async def start_story(request: StartStoryRequest):
    """开始一个新故事"""
    try:
        result = service.start_story(
            world=request.world,
            opening=request.opening,
            title=request.title
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/continue", response_model=ContinueStoryResponse)
async def continue_story(request: ContinueStoryRequest):
    """继续故事"""
    try:
        story_id = UUID(request.story_id)
        result = service.continue_story(
            story_id=story_id,
            user_choice=request.user_choice
        )
        return result
    except ValueError:
        raise HTTPException(status_code=400, detail="无效的故事ID")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{story_id}/history")
async def get_history(story_id: str):
    """获取单个故事的历史记录"""
    try:
        story_id_uuid = UUID(story_id)
        story = service.story_repo.get_by_id(story_id_uuid)
        if not story:
            raise HTTPException(status_code=404, detail="故事不存在")
        
        turns = service.turn_repo.get_by_story(story_id_uuid)
        return {
            "story_id": story_id,
            "title": story.title,
            "world": story.world.value,
            "created_at": story.created_at.isoformat(),
            "turns": [
                {
                    "turn_number": t.turn_number,
                    "user_choice": t.user_choice,
                    "narrative": t.narrative,
                    "choices": t.choices
                }
                for t in turns
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/history/all")
async def get_all_stories():
    """获取所有故事列表"""
    try:
        stories = service.story_repo.get_all()
        return {
            "stories": [
                {
                    "story_id": str(s.id),
                    "title": s.title,
                    "world": s.world.value,
                    "summary": s.summary or f"故事创建于 {s.created_at.strftime('%Y-%m-%d')}",
                    "created_at": s.created_at.isoformat(),
                    "turn_count": len(s.turns) if s.turns else 0
                }
                for s in stories
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))