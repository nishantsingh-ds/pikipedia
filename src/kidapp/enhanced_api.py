"""
Enhanced WonderBot API with authentication, quiz generation, and session management
"""

import os
import uuid
import logging
import hashlib
import requests
import json
from functools import lru_cache
from datetime import datetime
from typing import Optional, List, Dict, Any

from io import BytesIO
from PIL import Image
from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException, status
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from .crew import KidSafeAppCrew
from .models import *
from .auth import get_current_user, register_user, login_user
from .quiz_generator import generate_quiz_from_explanation, save_quiz_to_memory, get_quiz_by_id, submit_quiz_attempt
from openai import OpenAI
import base64

# ——— Logging setup ———
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ——— App & upload directory ———
app = FastAPI(
    title="WonderBot Enhanced API",
    version="2.0.0",
    description="AI-powered educational web app for kids with authentication, quizzes, and session management."
)

# Add CORS middleware for deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = os.path.join(os.getcwd(), "uploaded_images")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Mount static files for uploaded_images directory
app.mount("/uploaded_images", StaticFiles(directory=UPLOAD_DIR), name="uploaded_images")

# Mount static files for frontend assets
app.mount("/static", StaticFiles(directory="src/kidapp/static"), name="static")

# Simple cache for fast path responses
response_cache = {}

# Security
security = HTTPBearer()

# ——— Authentication Endpoints ———

@app.post("/auth/register", response_class=JSONResponse)
async def register(user_data: UserCreate):
    """Register a new user."""
    try:
        user = register_user(user_data)
        return {"message": "User registered successfully", "user": user}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Registration failed: {e}")
        raise HTTPException(status_code=500, detail="Registration failed")

@app.post("/auth/login", response_class=JSONResponse)
async def login(login_data: UserLogin):
    """Login a user."""
    try:
        result = login_user(login_data)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Login failed: {e}")
        raise HTTPException(status_code=500, detail="Login failed")

@app.get("/auth/me", response_class=JSONResponse)
async def get_current_user_info(current_user: UserResponse = Depends(get_current_user)):
    """Get current user information."""
    return {"user": current_user}

# ——— Session Management ———

def save_session_data(user_id: str, topic: str, explanation: str, diagram_url: Optional[str] = None, audio_url: Optional[str] = None, age: Optional[int] = None, interests: Optional[str] = None):
    """Save session data to memory storage."""
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

@app.get("/sessions/{user_id}", response_class=JSONResponse)
async def get_user_sessions(user_id: str, current_user: UserResponse = Depends(get_current_user)):
    """Get all sessions for a user."""
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this user's sessions")
    
    sessions = memory_storage.sessions.get(user_id, [])
    return {"sessions": sessions}

# ——— Quiz Endpoints ———

@app.post("/quiz/generate", response_class=JSONResponse)
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
        logger.error(f"Quiz generation failed: {e}")
        raise HTTPException(status_code=500, detail="Quiz generation failed")

@app.get("/quiz/{quiz_id}", response_class=JSONResponse)
async def get_quiz(quiz_id: str, current_user: UserResponse = Depends(get_current_user)):
    """Get a quiz by ID."""
    quiz = get_quiz_by_id(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    return {"quiz": quiz}

@app.post("/quiz/{quiz_id}/submit", response_class=JSONResponse)
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
        logger.error(f"Quiz submission failed: {e}")
        raise HTTPException(status_code=500, detail="Quiz submission failed")

@app.get("/quiz/user/{user_id}/attempts", response_class=JSONResponse)
async def get_user_quiz_attempts(user_id: str, current_user: UserResponse = Depends(get_current_user)):
    """Get all quiz attempts for a user."""
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this user's attempts")
    
    attempts = memory_storage.quiz_attempts.get(user_id, [])
    return {"attempts": attempts}

# ——— Enhanced Learning Endpoints ———

@app.get("/learning/progress/{user_id}", response_class=JSONResponse)
async def get_learning_progress(user_id: str, current_user: UserResponse = Depends(get_current_user)):
    """Get learning progress for a user."""
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this user's progress")
    
    progress = memory_storage.learning_progress.get(user_id, {})
    return {"progress": progress}

@app.get("/learning/recommendations/{user_id}", response_class=JSONResponse)
async def get_learning_recommendations(user_id: str, current_user: UserResponse = Depends(get_current_user)):
    """Get personalized learning recommendations."""
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this user's recommendations")
    
    # Simple recommendation logic based on user interests and progress
    user = current_user
    recommendations = []
    
    if user.interests:
        interests = user.interests.split(",")
        for interest in interests[:3]:  # Top 3 interests
            recommendations.append({
                "topic": interest.strip(),
                "reason": f"Based on your interest in {interest.strip()}",
                "difficulty": "medium"
            })
    
    return {"recommendations": recommendations}

# ——— Original WonderBot Endpoints (Enhanced) ———

def is_simple_question(topic: str) -> bool:
    """Check if the question is simple enough for fast path."""
    simple_keywords = [
        "what is", "what are", "how do", "why do", "what makes", 
        "what causes", "how does", "why does", "what does"
    ]
    topic_lower = topic.lower()
    return any(keyword in topic_lower for keyword in simple_keywords)

def fast_path_response(topic: str, age: int = None, interests: str = None) -> dict:
    """Generate a quick response for simple questions using direct OpenAI call."""
    try:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            return {"error": "OpenAI API key not configured"}
        
        client = OpenAI(api_key=openai_api_key)
        
        # Create a simple, direct prompt
        age_context = f" for a {age}-year-old child" if age else " for children aged 6-12"
        interests_context = f" who loves {interests}" if interests else ""
        
        prompt = f"""You are a friendly teacher explaining things to kids. 
        Explain this topic in a simple, fun way{age_context}{interests_context}:
        
        {topic}
        
        Keep it short (2-3 sentences), friendly, and easy to understand. 
        Use simple words and maybe a fun example."""
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7
        )
        
        content = response.choices[0].message.content.strip()
        
        # Clean up any JSON formatting if present
        if content.startswith('{"') or content.startswith('{'):
            try:
                parsed = json.loads(content)
                if 'result' in parsed:
                    content = parsed['result']
                elif 'content' in parsed:
                    content = parsed['content']
            except:
                pass
        
        # Generate diagram and audio for the fast path response
        dalle_prefix = "Create a simple, colorful diagram for kids that illustrates: "
        max_explanation_len = 4000 - len(dalle_prefix)
        dalle_prompt = dalle_prefix + content[:max_explanation_len]
        diagram_result = generate_diagram_with_dalle(dalle_prompt)
        
        # Truncate content for TTS to 4096 characters
        tts_text = content[:4096]
        audio_url = generate_audio_with_tts(tts_text)
        
        return {
            "result": content,
            "diagram_url": diagram_result["diagram_url"],
            "diagram_error": diagram_result["diagram_error"],
            "audio_url": audio_url,
            "fast_path": True
        }
        
    except Exception as e:
        logger.error(f"Fast path failed: {e}")
        return None

def fast_path_image_analysis(image_path: str, age: int = None, interests: str = None) -> dict:
    """Generate a quick response for image analysis using direct OpenAI Vision API call."""
    try:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            return {"error": "OpenAI API key not configured"}
        
        client = OpenAI(api_key=openai_api_key)
        
        # Create a simple, direct prompt
        age_context = f" for a {age}-year-old child" if age else " for children aged 6-12"
        interests_context = f" who loves {interests}" if interests else ""
        
        prompt = f"""You are a friendly teacher explaining things to kids. 
        Look at this image and explain what you see in a simple, fun way{age_context}{interests_context}.
        
        Keep it short (2-3 sentences), friendly, and easy to understand. 
        Use simple words and maybe a fun example."""
        
        # Read the image file
        with open(image_path, "rb") as image_file:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64.b64encode(image_file.read()).decode('utf-8')}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=150,
                temperature=0.7
            )
        
        content = response.choices[0].message.content.strip()
        
        # Clean up any JSON formatting if present
        if content.startswith('{"') or content.startswith('{'):
            try:
                parsed = json.loads(content)
                if 'result' in parsed:
                    content = parsed['result']
                elif 'content' in parsed:
                    content = parsed['content']
            except:
                pass
        
        # Generate diagram and audio for the fast path response
        dalle_prefix = "Create a simple, colorful diagram for kids that illustrates: "
        max_explanation_len = 4000 - len(dalle_prefix)
        dalle_prompt = dalle_prefix + content[:max_explanation_len]
        diagram_result = generate_diagram_with_dalle(dalle_prompt)
        
        # Truncate content for TTS to 4096 characters
        tts_text = content[:4096]
        audio_url = generate_audio_with_tts(tts_text)
        
        return {
            "result": content,
            "diagram_url": diagram_result["diagram_url"],
            "diagram_error": diagram_result["diagram_error"],
            "audio_url": audio_url,
            "fast_path": True
        }
        
    except Exception as e:
        logger.error(f"Fast path image analysis failed: {e}")
        return None

def generate_diagram_with_dalle(prompt: str) -> dict:
    """Generate a diagram using OpenAI DALL-E and return the local image URL with error handling."""
    try:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            logger.error("❌ OPENAI_API_KEY not found in environment")
            return {
                "diagram_url": "https://placehold.co/400x300?text=No+API+Key",
                "diagram_error": "API key not configured. Please check your OpenAI API key."
            }
        
        logger.info(f"🎨 Generating DALL-E diagram with prompt: {prompt[:100]}...")
        client = OpenAI(api_key=openai_api_key)
        
        # Add safety check for prompt length
        if len(prompt) > 4000:
            prompt = prompt[:4000]
            logger.info("📝 Truncated DALL-E prompt to fit limits")
        
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        
        url = getattr(response.data[0], 'url', None)
        if not url:
            logger.error("❌ DALL-E response missing URL")
            return {
                "diagram_url": "https://placehold.co/400x300?text=No+Diagram+Available",
                "diagram_error": "Sorry, we couldn't generate a diagram for this topic. Please try a different question!"
            }
        
        # Download and save the image locally
        logger.info(f"📥 Downloading DALL-E image from: {url}")
        try:
            img_response = requests.get(url, timeout=30)  # Add timeout
            if img_response.status_code == 200:
                # Generate a unique filename
                img_filename = f"diagram_{uuid.uuid4().hex}.png"
                img_path = os.path.join(UPLOAD_DIR, img_filename)
                
                # Ensure directory exists
                os.makedirs(UPLOAD_DIR, exist_ok=True)
                
                # Save the image
                with open(img_path, "wb") as f:
                    f.write(img_response.content)
                
                # Return local URL
                local_url = f"/uploaded_images/{img_filename}"
                logger.info(f"✅ DALL-E diagram saved locally: {local_url}")
                return {
                    "diagram_url": local_url,
                    "diagram_error": None
                }
            else:
                logger.error(f"❌ Failed to download DALL-E image: {img_response.status_code}")
                return {
                    "diagram_url": "https://placehold.co/400x300?text=Download+Failed",
                    "diagram_error": "Sorry, we couldn't save the diagram. Please try again!"
                }
        except Exception as e:
            logger.error(f"❌ Error downloading DALL-E image: {e}")
            return {
                "diagram_url": "https://placehold.co/400x300?text=Download+Error",
                "diagram_error": "Sorry, we couldn't save the diagram. Please try again!"
            }
            
    except Exception as e:
        logger.error(f"❌ DALL-E generation failed: {e}")
        return {
            "diagram_url": "https://placehold.co/400x300?text=Generation+Failed",
            "diagram_error": f"Sorry, we couldn't generate a diagram. Error: {str(e)}"
        }

def generate_audio_with_tts(text: str) -> str:
    """Generate audio using OpenAI TTS and return the local audio URL with error handling."""
    try:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            logger.error("❌ OPENAI_API_KEY not found in environment")
            return "/uploaded_images/audio_error.mp3"
        
        # Truncate text to fit TTS limits
        if len(text) > 4096:
            text = text[:4096]
            logger.info("📝 Truncated TTS text to fit limits")
        
        logger.info(f"🔊 Generating TTS audio for text: {text[:100]}...")
        client = OpenAI(api_key=openai_api_key)
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )
        
        # Generate a unique filename
        audio_filename = f"audio_{uuid.uuid4().hex}.mp3"
        audio_path = os.path.join(UPLOAD_DIR, audio_filename)
        
        # Ensure directory exists
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        
        # Save the audio file
        response.stream_to_file(audio_path)
        
        # Return local URL
        local_url = f"/uploaded_images/{audio_filename}"
        logger.info(f"✅ TTS audio saved locally: {local_url}")
        return local_url
        
    except Exception as e:
        logger.error(f"❌ TTS generation failed: {e}")
        return "/uploaded_images/audio_error.mp3"

def clean_crewai_result(result) -> str:
    """Extract clean text from CrewAI result, removing JSON formatting."""
    if isinstance(result, dict):
        # Look for the actual content in common keys
        for key in ['result', 'content', 'output', 'text']:
            if key in result and result[key]:
                content = str(result[key])
                # Remove JSON formatting if present
                if content.startswith('{"') or content.startswith('{'):
                    try:
                        parsed = json.loads(content)
                        if 'result' in parsed:
                            return str(parsed['result'])
                        elif 'content' in parsed:
                            return str(parsed['content'])
                    except:
                        pass
                return content
        
        # If no specific key found, return the whole result as string
        return str(result)
    else:
        return str(result)

@app.post("/generate", response_class=JSONResponse)
async def generate(
    topic: str = Form(None, description="The topic or question to explain (optional if image is provided)"),
    image: UploadFile = File(None, description="Optional image to analyze"),
    age: int = Form(None, description="Child's age (optional)"),
    interests: str = Form(None, description="Comma-separated interests (optional)"),
    current_user: Optional[UserResponse] = Depends(get_current_user)
):
    """
    Generate a kid-friendly explanation for either:
    - An uploaded image (if image is provided)
    - A text topic/question (if topic is provided)
    
    Now with session tracking and user authentication!
    """
    # Enforce that only one of image or topic is provided
    if (image and topic) or (not image and not topic):
        return JSONResponse(
            status_code=400,
            content={"error": "Please provide either a question or an image, but not both."}
        )
    
    # Check cache for simple text questions
    if topic and not image:
        cache_key = f"{topic}_{age}_{interests}"
        if cache_key in response_cache:
            logger.info("🚀 Returning cached response")
            return {"outputs": response_cache[cache_key]}
    
    # 1. Build the inputs dict
    inputs = {}
    
    if image:
        # Image analysis mode - use CrewAI workflow
        ext = os.path.splitext(image.filename or "")[1] or ".png"
        fname = f"{uuid.uuid4().hex}{ext}"
        fpath = os.path.join(UPLOAD_DIR, fname)

        contents = await image.read()
        with open(fpath, "wb") as f:
            f.write(contents)

        md5 = hashlib.md5(contents).hexdigest()
        logger.info(f"\U0001F4E5 Uploaded image saved to {fpath!r} ({len(contents)} bytes; md5={md5})")

        try:
            img = Image.open(BytesIO(contents)).convert("RGB")
            logger.info(f"\U0001F4CF PIL sees size={img.size}, mode={img.mode}")
        except Exception:
            logger.exception("❌ Failed to open/dump the uploaded image")

        # Check cache for image analysis (using file hash as key)
        image_cache_key = f"image_{md5}_{age}_{interests}"
        if image_cache_key in response_cache:
            logger.info("🚀 Returning cached image analysis response")
            return {"outputs": response_cache[image_cache_key]}
        
        # Try fast path for image analysis first
        logger.info("⚡ Trying fast path for image analysis...")
        fast_result = fast_path_image_analysis(fpath, age, interests)
        if fast_result and not fast_result.get("error"):
            logger.info("✅ Fast path image analysis completed successfully")
            # Cache the result
            response_cache[image_cache_key] = fast_result
            
            # Save session data if user is authenticated
            if current_user:
                save_session_data(
                    user_id=current_user.id,
                    topic=f"Image Analysis: {image.filename}",
                    explanation=fast_result["result"],
                    diagram_url=fast_result["diagram_url"],
                    audio_url=fast_result["audio_url"],
                    age=age,
                    interests=interests
                )
            
            return {"outputs": fast_result}
        
        # Fallback to CrewAI workflow if fast path fails
        logger.info("🔄 Fast path failed, falling back to CrewAI workflow...")
        inputs = {"image_path": fpath, "mode": "image_analysis", "age": age, "interests": interests}
        logger.info(f"🚀 Starting CrewAI image analysis workflow with inputs: {inputs}")
        try:
            logger.info("📋 Creating CrewAI instance for image analysis...")
            crew_instance = KidSafeAppCrew()
            crew_instance._inputs = inputs
            logger.info("🔧 Building crew for image analysis...")
            crew = crew_instance.crew()
            logger.info("⚡ Starting crew.kickoff() for image analysis...")
            result = crew.kickoff(inputs=inputs)
            logger.info("✅ CrewAI image analysis completed successfully")
            
            # Clean the result to get just the content
            explanation = clean_crewai_result(result)
            
            # Generate diagram and audio for the image analysis
            dalle_prefix = "Create a simple, colorful diagram for kids that illustrates: "
            max_explanation_len = 4000 - len(dalle_prefix)
            dalle_prompt = dalle_prefix + explanation[:max_explanation_len]
            diagram_result = generate_diagram_with_dalle(dalle_prompt)
            
            # Truncate explanation for TTS to 4096 characters
            tts_text = explanation[:4096]
            audio_url = generate_audio_with_tts(tts_text)
            
            final_result = {
                "result": explanation,
                "diagram_url": diagram_result["diagram_url"],
                "diagram_error": diagram_result["diagram_error"],
                "audio_url": audio_url
            }
            
            # Cache the result
            response_cache[image_cache_key] = final_result
            
            # Save session data if user is authenticated
            if current_user:
                save_session_data(
                    user_id=current_user.id,
                    topic=f"Image Analysis: {image.filename}",
                    explanation=explanation,
                    diagram_url=diagram_result["diagram_url"],
                    audio_url=audio_url,
                    age=age,
                    interests=interests
                )
            
            logger.info("🎉 Image analysis multimodal processing completed")
            
        except Exception as e:
            logger.exception("❌ CrewAI image analysis execution or multimodal generation failed")
            return JSONResponse(
                status_code=500,
                content={"error": str(e)}
            )
        return {"outputs": final_result}
    elif topic:
        # Check if this is a simple question for fast path
        if is_simple_question(topic):
            logger.info("⚡ Using fast path for simple question")
            fast_result = fast_path_response(topic, age, interests)
            if fast_result and not fast_result.get("error"):
                # Cache the result
                cache_key = f"{topic}_{age}_{interests}"
                response_cache[cache_key] = fast_result
                
                # Save session data if user is authenticated
                if current_user:
                    save_session_data(
                        user_id=current_user.id,
                        topic=topic,
                        explanation=fast_result["result"],
                        diagram_url=fast_result["diagram_url"],
                        audio_url=fast_result["audio_url"],
                        age=age,
                        interests=interests
                    )
                
                return {"outputs": fast_result}
        
        # Text mode - use CrewAI workflow
        inputs = {"topic": topic, "age": age, "interests": interests}
        logger.info(f"🚀 Starting CrewAI workflow with inputs: {inputs}")
        try:
            logger.info("📋 Creating CrewAI instance...")
            crew_instance = KidSafeAppCrew()
            crew_instance._inputs = inputs
            logger.info("🔧 Building crew...")
            crew = crew_instance.crew()
            logger.info("⚡ Starting crew.kickoff()...")
            result = crew.kickoff(inputs=inputs)
            logger.info("✅ CrewAI completed successfully")
            
            # Clean the result to get just the content
            explanation = clean_crewai_result(result)
            
            # Generate diagram and audio
            dalle_prefix = "Create a simple, colorful diagram for kids that illustrates: "
            max_explanation_len = 4000 - len(dalle_prefix)
            dalle_prompt = dalle_prefix + explanation[:max_explanation_len]
            diagram_result = generate_diagram_with_dalle(dalle_prompt)
            
            # Truncate explanation for TTS to 4096 characters
            tts_text = explanation[:4096]
            audio_url = generate_audio_with_tts(tts_text)
            
            final_result = {
                "result": explanation,
                "diagram_url": diagram_result["diagram_url"],
                "diagram_error": diagram_result["diagram_error"],
                "audio_url": audio_url
            }
            
            # Cache the result
            cache_key = f"{topic}_{age}_{interests}"
            response_cache[cache_key] = final_result
            
            # Save session data if user is authenticated
            if current_user:
                save_session_data(
                    user_id=current_user.id,
                    topic=topic,
                    explanation=explanation,
                    diagram_url=diagram_result["diagram_url"],
                    audio_url=audio_url,
                    age=age,
                    interests=interests
                )
            
            logger.info("🎉 Multimodal processing completed")
        except Exception as e:
            logger.exception("❌ CrewAI execution or multimodal generation failed")
            return JSONResponse(
                status_code=500,
                content={"error": str(e)}
            )
        return {"outputs": final_result}

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the frontend HTML page."""
    with open("src/kidapp/static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read()) 