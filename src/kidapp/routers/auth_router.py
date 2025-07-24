"""
Authentication router for WonderBot
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ..models import UserCreate, UserLogin, UserResponse
from ..auth import register_user, login_user, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_class=JSONResponse)
async def register(user_data: UserCreate):
    """Register a new user."""
    try:
        user = register_user(user_data)
        return {"message": "User registered successfully", "user": user}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Registration failed")

@router.post("/login", response_class=JSONResponse)
async def login(login_data: UserLogin):
    """Login a user."""
    try:
        result = login_user(login_data)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Login failed")

@router.get("/me", response_class=JSONResponse)
async def get_current_user_info(current_user: UserResponse = Depends(get_current_user)):
    """Get current user information."""
    return {"user": current_user} 