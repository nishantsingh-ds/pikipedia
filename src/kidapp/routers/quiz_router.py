"""
Quiz router for WonderBot
"""

from fastapi import APIRouter, HTTPException, Depends, Form
from fastapi.responses import JSONResponse
from typing import Dict

from ..models import UserResponse, DifficultyLevel
from ..auth import get_current_user
from ..quiz_generator import (
    generate_quiz_from_explanation, 
    save_quiz_to_memory, 
    get_quiz_by_id, 
    submit_quiz_attempt
)

router = APIRouter(prefix="/quiz", tags=["Quizzes"])

@router.post("/generate", response_class=JSONResponse)
async def generate_quiz(
    topic: str = Form(...),
    explanation: str = Form(...),
    difficulty: DifficultyLevel = Form(DifficultyLevel.MEDIUM),
    num_questions: int = Form(5),
    current_user: UserResponse = Depends(get_current_user)
):
    """Generate a quiz from an explanation."""
    try:
        quiz = generate_quiz_from_explanation(
            explanation=explanation,
            topic=topic,
            difficulty=difficulty,
            num_questions=num_questions
        )
        
        # Save quiz to memory
        save_quiz_to_memory(quiz)
        
        return {"quiz": quiz}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Quiz generation failed")

@router.get("/{quiz_id}", response_class=JSONResponse)
async def get_quiz(quiz_id: str, current_user: UserResponse = Depends(get_current_user)):
    """Get a quiz by ID."""
    quiz = get_quiz_by_id(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    return {"quiz": quiz}

@router.post("/{quiz_id}/submit", response_class=JSONResponse)
async def submit_quiz(
    quiz_id: str,
    answers: Dict[str, str],
    current_user: UserResponse = Depends(get_current_user)
):
    """Submit quiz answers and get results."""
    try:
        result = submit_quiz_attempt(quiz_id, current_user.id, answers)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Quiz submission failed")

@router.get("/user/{user_id}/attempts", response_class=JSONResponse)
async def get_user_quiz_attempts(user_id: str, current_user: UserResponse = Depends(get_current_user)):
    """Get all quiz attempts for a user."""
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this user's attempts")
    
    from ..models import memory_storage
    attempts = memory_storage.quiz_attempts.get(user_id, [])
    return {"attempts": attempts} 