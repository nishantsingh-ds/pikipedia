import os
import uuid
import logging
import hashlib
import requests

from io import BytesIO
from PIL import Image
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not available, use system environment variables

from kidapp.crew import KidSafeAppCrew
from openai import OpenAI
import base64

# ——— Logging setup ———
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ——— App & upload directory ———
app = FastAPI(
    title="Kid Educate App POC API",
    version="0.1.0",
    description="Proof-of-concept API to run the KidSafeAppCrew and return results."
)

# Add CORS middleware for deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
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

# Note: Image analysis is now handled by CrewAI agents instead of direct OpenAI calls

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
            img_response = requests.get(url)
            if img_response.status_code == 200:
                # Generate a unique filename
                img_filename = f"diagram_{uuid.uuid4().hex}.png"
                img_path = os.path.join(UPLOAD_DIR, img_filename)
                
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
                logger.error(f"❌ Failed to download DALL-E image: HTTP {img_response.status_code}")
                return {
                    "diagram_url": "https://placehold.co/400x300?text=Download+Failed",
                    "diagram_error": "Sorry, we couldn't download the generated diagram. Please try again!"
                }
        except Exception as e:
            logger.error(f"❌ Error downloading DALL-E image: {str(e)}")
            return {
                "diagram_url": "https://placehold.co/400x300?text=Download+Error",
                "diagram_error": "Sorry, there was an error downloading the diagram. Please try again!"
            }
            
    except Exception as e:
        logger.error(f"❌ DALL-E error: {str(e)}")
        return {
            "diagram_url": "https://placehold.co/400x300?text=DALL-E+Error",
            "diagram_error": "Sorry, we couldn't generate a diagram for this topic. Please try a different question!"
        }

def generate_audio_with_tts(text: str) -> str:
    """Generate audio using OpenAI TTS and return the audio URL."""
    try:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            logger.error("❌ OPENAI_API_KEY not found in environment")
            return "https://placehold.co/1s.mp3?text=No+API+Key"
        
        logger.info(f"🔊 Generating TTS audio for text: {text[:100]}...")
        client = OpenAI(api_key=openai_api_key)
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )
        # Save the audio to a file and return the file path or URL
        audio_path = os.path.join(UPLOAD_DIR, f"audio_{uuid.uuid4().hex}.mp3")
        with open(audio_path, "wb") as f:
            f.write(response.content)
        
        audio_url = f"/uploaded_images/{os.path.basename(audio_path)}"
        logger.info(f"✅ TTS audio generated: {audio_url}")
        return audio_url
    except Exception as e:
        logger.error(f"❌ TTS error: {str(e)}")
        return "https://placehold.co/1s.mp3?text=TTS+Error"

@app.post("/generate", response_class=JSONResponse)
async def generate(
    topic: str = Form(None, description="The topic or question to explain (optional if image is provided)"),
    image: UploadFile = File(None, description="Optional image to analyze"),
    age: int = Form(None, description="Child's age (optional)"),
    interests: str = Form(None, description="Comma-separated interests (optional)")
):
    """
    Generate a kid-friendly explanation for either:
    - An uploaded image (if image is provided)
    - A text topic/question (if topic is provided)
    """
    # Enforce that only one of image or topic is provided
    if (image and topic) or (not image and not topic):
        return JSONResponse(
            status_code=400,
            content={"error": "Please provide either a question or an image, but not both."}
    )
    
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

        # Use CrewAI workflow for image analysis
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
            
            # Convert CrewOutput to dict if needed
            if not isinstance(result, dict):
                if hasattr(result, 'dict') and callable(getattr(result, 'dict')):
                    result = result.dict()
                elif hasattr(result, '__dict__'):
                    result = dict(result.__dict__)
                else:
                    result = {"result": str(result)}
            
            logger.info("🔄 Processing image analysis result for multimodal output...")
            # Extract explanation for multimodal output
            explanation = result.get("result") or result.get("content") or str(result)
            
            # Generate diagram and audio for the image analysis
            dalle_prefix = "Create a simple, colorful diagram for kids that illustrates: "
            max_explanation_len = 4000 - len(dalle_prefix)
            dalle_prompt = dalle_prefix + explanation[:max_explanation_len]
            diagram_result = generate_diagram_with_dalle(dalle_prompt)
            
            # Truncate explanation for TTS to 4096 characters
            tts_text = explanation[:4096]
            audio_url = generate_audio_with_tts(tts_text)
            
            result["diagram_url"] = diagram_result["diagram_url"]
            result["diagram_error"] = diagram_result["diagram_error"]
            result["audio_url"] = audio_url
            logger.info("🎉 Image analysis multimodal processing completed")
            
        except Exception as e:
            logger.exception("❌ CrewAI image analysis execution or multimodal generation failed")
            return JSONResponse(
                status_code=500,
                content={"error": str(e)}
            )
        return {"outputs": result}
    elif topic:
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
            # Convert CrewOutput to dict if needed
            if not isinstance(result, dict):
                if hasattr(result, 'dict') and callable(getattr(result, 'dict')):
                    result = result.dict()
                elif hasattr(result, '__dict__'):
                    result = dict(result.__dict__)
                else:
                    result = {"result": str(result)}
            logger.info("🔄 Processing result for multimodal output...")
            # Extract explanation for multimodal output
            explanation = result.get("content") or result.get("result") or str(result)
            # Generate diagram and audio
            dalle_prefix = "Create a simple, colorful diagram for kids that illustrates: "
            max_explanation_len = 4000 - len(dalle_prefix)
            dalle_prompt = dalle_prefix + explanation[:max_explanation_len]
            diagram_result = generate_diagram_with_dalle(dalle_prompt)
            # Truncate explanation for TTS to 4096 characters
            tts_text = explanation[:4096]
            audio_url = generate_audio_with_tts(tts_text)
            result["diagram_url"] = diagram_result["diagram_url"]
            result["diagram_error"] = diagram_result["diagram_error"]
            result["audio_url"] = audio_url
            logger.info("🎉 Multimodal processing completed")
        except Exception as e:
            logger.exception("❌ CrewAI execution or multimodal generation failed")
            return JSONResponse(
                status_code=500,
                content={"error": str(e)}
            )
        return {"outputs": result}

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the frontend HTML page."""
    with open("src/kidapp/static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())
