"""
Database models for WonderBot - AI-powered educational web app for kids
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum

class UserRole(str, Enum):
    STUDENT = "student"
    PARENT = "parent"
    TEACHER = "teacher"

class QuestionType(str, Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    FILL_BLANK = "fill_blank"
    SHORT_ANSWER = "short_answer"

class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

# Pydantic Models for API
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., regex=r"^[^@]+@[^@]+\.[^@]+$")
    password: str = Field(..., min_length=6)
    age: Optional[int] = Field(None, ge=3, le=18)
    interests: Optional[str] = None
    role: UserRole = UserRole.STUDENT

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    age: Optional[int] = None
    interests: Optional[str] = None
    role: UserRole
    created_at: datetime
    last_login: Optional[datetime] = None

class SessionData(BaseModel):
    user_id: str
    topic: str
    explanation: str
    diagram_url: Optional[str] = None
    audio_url: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    age: Optional[int] = None
    interests: Optional[str] = None

class QuizQuestion(BaseModel):
    question: str
    question_type: QuestionType
    correct_answer: str
    options: Optional[List[str]] = None  # For multiple choice
    explanation: Optional[str] = None
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM

class Quiz(BaseModel):
    id: str
    title: str
    topic: str
    questions: List[QuizQuestion]
    difficulty: DifficultyLevel
    created_at: datetime = Field(default_factory=datetime.utcnow)
    estimated_time: int = Field(..., description="Estimated time in minutes")

class QuizAttempt(BaseModel):
    quiz_id: str
    user_id: str
    score: float
    total_questions: int
    correct_answers: int
    time_taken: int  # in seconds
    completed_at: datetime = Field(default_factory=datetime.utcnow)
    answers: Dict[str, str] = Field(..., description="Question ID to answer mapping")

class LearningProgress(BaseModel):
    user_id: str
    topic: str
    sessions_count: int = 0
    total_time_spent: int = 0  # in seconds
    quiz_attempts: int = 0
    average_quiz_score: float = 0.0
    last_accessed: datetime = Field(default_factory=datetime.utcnow)
    mastery_level: float = Field(0.0, ge=0.0, le=1.0, description="0.0 to 1.0 mastery")

class Achievement(BaseModel):
    id: str
    name: str
    description: str
    icon: str
    criteria: Dict[str, Any]
    unlocked_at: Optional[datetime] = None

# In-memory storage (replace with database in production)
class MemoryStorage:
    def __init__(self):
        self.users: Dict[str, UserResponse] = {}
        self.sessions: Dict[str, List[SessionData]] = {}
        self.quizzes: Dict[str, Quiz] = {}
        self.quiz_attempts: Dict[str, List[QuizAttempt]] = {}
        self.learning_progress: Dict[str, Dict[str, LearningProgress]] = {}
        self.achievements: Dict[str, List[Achievement]] = {}

# Global memory storage instance
memory_storage = MemoryStorage() 