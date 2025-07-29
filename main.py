"""
LeetCode AI Coach - Backend API
Provides AI-powered coaching feedback for LeetCode problems
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import openai
import os
import logging
import json
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    logger.warning("OpenAI API key not found. Fallback responses will be used.")

# FastAPI app
app = FastAPI(
    title="LeetCode AI Coach API",
    version="1.0.0",
    description="AI-powered coaching feedback for LeetCode problems"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class AnalyzeRequest(BaseModel):
    problemSlug: str
    code: str

class Recommendation(BaseModel):
    title: str
    link: str

class FeedbackResponse(BaseModel):
    approach: str
    gaps: List[str]
    principles: List[str]
    recommendations: List[Recommendation]

class AnalyzeResponse(BaseModel):
    feedback: FeedbackResponse

# Routes
@app.get("/")
async def root():
    return {
        "message": "LeetCode AI Coach API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "openai_configured": bool(openai.api_key)}

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_code(request: AnalyzeRequest):
    """
    Analyze user's LeetCode solution and provide AI coaching feedback
    """
    try:
        # Validate input
        if not request.problemSlug or not request.code.strip():
            raise HTTPException(status_code=400, detail="Problem slug and code are required")
        
        logger.info(f"Analyzing code for problem: {request.problemSlug}")
        
        # Generate AI feedback
        feedback = await generate_feedback(request.problemSlug, request.code)
        
        return AnalyzeResponse(feedback=feedback)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing code: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

async def generate_feedback(problem_slug: str, code: str) -> FeedbackResponse:
    """
    Generate comprehensive feedback using OpenAI
    """
    # If no OpenAI key, return fallback immediately
    if not openai.api_key:
        logger.info("No OpenAI key found, returning fallback feedback")
        return create_fallback_feedback(problem_slug)
    
    try:
        # Create the analysis prompt
        prompt = f"""
You are an expert programming coach analyzing a LeetCode solution. 

Problem: {problem_slug}
Code:
```
{code}
```

Please provide coaching feedback in exactly this JSON format:
{{
  "approach": "One sentence describing the algorithmic approach used",
  "gaps": ["First conceptual gap using Feynman technique", "Second conceptual gap", "Third conceptual gap"],
  "principles": ["First first-principles optimization tip", "Second optimization tip", "Third optimization tip"],
  "recommendations": [
    {{"title": "Problem Name", "link": "https://leetcode.com/problems/problem-slug/"}},
    {{"title": "Problem Name", "link": "https://leetcode.com/problems/problem-slug/"}},
    {{"title": "Problem Name", "link": "https://leetcode.com/problems/problem-slug/"}},
    {{"title": "Problem Name", "link": "https://leetcode.com/problems/problem-slug/"}},
    {{"title": "Problem Name", "link": "https://leetcode.com/problems/problem-slug/"}}
  ]
}}

Guidelines:
- Approach: Identify the main algorithm/pattern (e.g., "Two pointers technique for in-place array manipulation")
- Gaps: Explain missing concepts as if teaching a child (Feynman technique)
- Principles: Focus on fundamental optimizations (time/space complexity, clean code)
- Recommendations: Suggest 5 similar real LeetCode problems with actual links

Respond with ONLY the JSON, no additional text.
        """
        
        # Call OpenAI API with timeout
        try:
            response = await asyncio.wait_for(
                asyncio.create_task(openai.ChatCompletion.acreate(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful programming coach. Always respond with valid JSON only."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1000,
                    temperature=0.7
                )),
                timeout=15.0  # 15 second timeout
            )
        except asyncio.TimeoutError:
            logger.warning("OpenAI API timeout, using fallback")
            return create_fallback_feedback(problem_slug)
        except Exception as api_error:
            logger.warning(f"OpenAI API error: {str(api_error)}, using fallback")
            return create_fallback_feedback(problem_slug)
        
        # Parse the response
        feedback_text = response.choices[0].message.content.strip()
        
        # Try to parse as JSON
        try:
            feedback_data = json.loads(feedback_text)
        except json.JSONDecodeError as json_error:
            logger.warning(f"Failed to parse OpenAI response as JSON: {str(json_error)}, using fallback")
            return create_fallback_feedback(problem_slug)
        
        # Validate and create response
        try:
            feedback = FeedbackResponse(
                approach=feedback_data.get("approach", "Unable to determine approach"),
                gaps=feedback_data.get("gaps", ["Could not identify specific gaps"])[:3],
                principles=feedback_data.get("principles", ["Focus on correctness first", "Consider edge cases", "Optimize after working solution"])[:3],
                recommendations=[
                    Recommendation(
                        title=rec.get("title", "Related Problem"), 
                        link=rec.get("link", f"https://leetcode.com/problems/{problem_slug}/")
                    )
                    for rec in feedback_data.get("recommendations", [])[:5]
                ]
            )
            return feedback
        except Exception as validation_error:
            logger.warning(f"Error validating feedback response: {str(validation_error)}, using fallback")
            return create_fallback_feedback(problem_slug)
        
    except Exception as e:
        logger.error(f"Unexpected error generating feedback: {str(e)}")
        return create_fallback_feedback(problem_slug)

def create_fallback_feedback(problem_slug: str) -> FeedbackResponse:
    """
    Create fallback feedback when OpenAI fails
    """
    return FeedbackResponse(
        approach="This solution uses a straightforward approach - consider if there are more efficient patterns",
        gaps=[
            "Think about the time complexity - can you do better than checking every possibility?",
            "Consider what data structures might help you avoid repeated work",
            "Ask yourself: what information from previous steps can you reuse?"
        ],
        principles=[
            "Start with a working solution, then optimize step by step",
            "Look for patterns like two pointers, sliding window, or divide and conquer",
            "Test your solution with edge cases like empty inputs or single elements"
        ],
        recommendations=[
            Recommendation(title="Two Sum", link="https://leetcode.com/problems/two-sum/"),
            Recommendation(title="Valid Parentheses", link="https://leetcode.com/problems/valid-parentheses/"),
            Recommendation(title="Best Time to Buy and Sell Stock", link="https://leetcode.com/problems/best-time-to-buy-and-sell-stock/"),
            Recommendation(title="Maximum Subarray", link="https://leetcode.com/problems/maximum-subarray/"),
            Recommendation(title="Merge Two Sorted Lists", link="https://leetcode.com/problems/merge-two-sorted-lists/")
        ]
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 