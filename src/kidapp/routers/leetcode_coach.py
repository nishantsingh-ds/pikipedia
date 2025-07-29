"""
LeetCode AI Coach Router
Provides AI-powered coaching feedback for LeetCode problems
"""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import openai
import os
from dotenv import load_dotenv
import logging
import asyncio
import json

# Load environment variables
load_dotenv()

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

# Setup logging
logger = logging.getLogger(__name__)

# Add error handling for missing OpenAI key
if not openai.api_key:
    logger.warning("OpenAI API key not found. Fallback responses will be used.")

router = APIRouter(prefix="/api", tags=["leetcode-coach"])

# Global exception handler for this router
@router.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception in LeetCode coach: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error occurred while analyzing code",
            "error": "analysis_failed"
        }
    )

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

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_code(request: AnalyzeRequest):
    """
    Analyze user's LeetCode solution and provide AI coaching feedback
    """
    try:
        # Validate input
        if not request.problemSlug or not request.code.strip():
            raise HTTPException(status_code=400, detail="Problem slug and code are required")
        
        # Generate AI feedback
        feedback = await generate_feedback(request.problemSlug, request.code)
        
        return AnalyzeResponse(feedback=feedback)
        
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
            # Fallback response if JSON parsing fails
            logger.warning(f"Failed to parse OpenAI response as JSON: {str(json_error)}, using fallback")
            return create_fallback_feedback(problem_slug)
        
        # Validate and create response
        try:
            feedback = FeedbackResponse(
                approach=feedback_data.get("approach", "Unable to determine approach"),
                gaps=feedback_data.get("gaps", ["Could not identify specific gaps"])[:3],  # Limit to 3
                principles=feedback_data.get("principles", ["Focus on correctness first", "Consider edge cases", "Optimize after working solution"])[:3],  # Limit to 3
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
        # Return fallback response
        return create_fallback_feedback(problem_slug)

def create_fallback_feedback(problem_slug: str) -> FeedbackResponse:
    """
    Create fallback feedback when OpenAI fails
    """
    return FeedbackResponse(
        approach="Unable to analyze approach due to API limitations",
        gaps=[
            "Consider breaking down the problem into smaller steps",
            "Think about the data structures that best fit this problem",
            "Review the time and space complexity requirements"
        ],
        principles=[
            "Start with a brute force solution that works",
            "Look for patterns or repeated calculations to optimize",
            "Test your solution with edge cases"
        ],
        recommendations=[
            Recommendation(title="Two Sum", link="https://leetcode.com/problems/two-sum/"),
            Recommendation(title="Valid Parentheses", link="https://leetcode.com/problems/valid-parentheses/"),
            Recommendation(title="Best Time to Buy and Sell Stock", link="https://leetcode.com/problems/best-time-to-buy-and-sell-stock/"),
            Recommendation(title="Maximum Subarray", link="https://leetcode.com/problems/maximum-subarray/"),
            Recommendation(title="Merge Two Sorted Lists", link="https://leetcode.com/problems/merge-two-sorted-lists/")
        ]
    )