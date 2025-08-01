"""
Authentication system for WonderBot
"""

import hashlib
import secrets
import uuid
import re
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

from .models import UserCreate, UserResponse, UserLogin, memory_storage

# JWT Configuration
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

def validate_password_strength(password: str) -> dict:
    """Validate password strength and return detailed feedback."""
    errors = []
    suggestions = []
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    elif len(password) < 12:
        suggestions.append("Consider using a longer password (12+ characters)")
    
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")
    
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")
    
    if not re.search(r'\d', password):
        errors.append("Password must contain at least one number")
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        suggestions.append("Consider adding special characters for extra security")
    
    # Check for common patterns
    common_patterns = ['password', '123456', 'qwerty', 'admin', 'user']
    if any(pattern in password.lower() for pattern in common_patterns):
        errors.append("Password contains common patterns that are easily guessed")
    
    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "suggestions": suggestions
    }

def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return hash_password(plain_password) == hashed_password

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserResponse:
    """Get the current user from the JWT token."""
    token = credentials.credentials
    print(f"DEBUG: Token received: {token[:20]}...")  # Show first 20 chars
    
    payload = verify_token(token)
    if payload is None:
        print("DEBUG: Token verification failed")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    print(f"DEBUG: Token payload: {payload}")
    
    user_id = payload.get("sub")
    if user_id is None:
        print("DEBUG: No 'sub' field in token payload")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    print(f"DEBUG: Looking for user with ID: {user_id}")
    user = memory_storage.users.get(user_id)
    if user is None:
        print(f"DEBUG: User not found in memory storage. Available users: {list(memory_storage.users.keys())}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    print(f"DEBUG: User found: {user.username}")
    return user

def register_user(user_data: UserCreate) -> UserResponse:
    """Register a new user."""
    # Validate password strength
    password_validation = validate_password_strength(user_data.password)
    if not password_validation["is_valid"]:
        error_message = "Password validation failed: " + "; ".join(password_validation["errors"])
        if password_validation["suggestions"]:
            error_message += ". Suggestions: " + "; ".join(password_validation["suggestions"])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message
        )
    
    # Check if username already exists
    for user in memory_storage.users.values():
        if user.username == user_data.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        if user.email == user_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Create new user
    user_id = str(uuid.uuid4())
    hashed_password = hash_password(user_data.password)
    
    new_user = UserResponse(
        id=user_id,
        username=user_data.username,
        email=user_data.email,
        age=user_data.age,
        interests=user_data.interests,
        role=user_data.role,
        created_at=datetime.now(timezone.utc),
        last_login=None
    )
    
    # Store user with hashed password (in production, use a proper database)
    memory_storage.users[user_id] = new_user
    # Store password hash separately (in production, use a proper database)
    if not hasattr(memory_storage, 'password_hashes'):
        memory_storage.password_hashes = {}
    memory_storage.password_hashes[user_id] = hashed_password
    
    return new_user

def authenticate_user(login_data: UserLogin) -> Optional[UserResponse]:
    """Authenticate a user with username and password."""
    # Find user by username
    user = None
    for u in memory_storage.users.values():
        if u.username == login_data.username:
            user = u
            break
    
    if not user:
        print(f"DEBUG: User '{login_data.username}' not found")
        return None
    
    # Verify password against stored hash
    if not hasattr(memory_storage, 'password_hashes'):
        memory_storage.password_hashes = {}
    
    stored_hash = memory_storage.password_hashes.get(user.id)
    if not stored_hash:
        print(f"DEBUG: No password hash found for user '{login_data.username}'")
        return None
    
    if verify_password(login_data.password, stored_hash):
        print(f"DEBUG: Password verified for user '{login_data.username}'")
        return user
    else:
        print(f"DEBUG: Password verification failed for user '{login_data.username}'")
    
    return None

def login_user(login_data: UserLogin) -> dict:
    """Login a user and return access token."""
    user = authenticate_user(login_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login
    user.last_login = datetime.now(timezone.utc)
    memory_storage.users[user.id] = user
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    } 