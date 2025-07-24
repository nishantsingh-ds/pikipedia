"""
Session management router for WonderBot
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from ..models import UserResponse
from ..auth import get_current_user

router = APIRouter(prefix="/sessions", tags=["Sessions"])

def save_session_data(user_id: str, topic: str, explanation: str, diagram_url: str = None, audio_url: str = None, age: int = None, interests: str = None):
    """Save session data to memory storage."""
    from ..models import SessionData, memory_storage
    
    session_data = SessionData(
        user_id=user_id,
        topic=topic,
        explanation=explanation,
        diagram_url=diagram_url,
        audio_url=audio_url,
        age=age,
        interests=interests
    )
    
    if user_id not in memory_storage.sessions:
        memory_storage.sessions[user_id] = []
    memory_storage.sessions[user_id].append(session_data)

@router.get("/{user_id}", response_class=JSONResponse)
async def get_user_sessions(user_id: str, current_user: UserResponse = Depends(get_current_user)):
    """Get all sessions for a user."""
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this user's sessions")
    
    from ..models import memory_storage
    sessions = memory_storage.sessions.get(user_id, [])
    return {"sessions": sessions} 