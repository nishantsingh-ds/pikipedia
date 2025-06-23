# src/kidapp/agents/image_analyzer.py

import os
import base64
from pydantic import ConfigDict
from crewai import Agent
from typing import Any
from openai import OpenAI

def analyze_image_with_openai(image_path: str) -> str:
    """
    Analyze an image using OpenAI's GPT-4 Vision model
    
    Args:
        image_path: Path to the image file to analyze
        
    Returns:
        Detailed description of the image
    """
    # Check if OpenAI API key is available
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise RuntimeError(
            "Please set OPENAI_API_KEY in your environment to access OpenAI's GPT-4 Vision model."
        )

    # Initialize OpenAI client
    client = OpenAI(api_key=openai_api_key)

    # Read and encode the image
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        base64_image = base64.b64encode(image_data).decode('utf-8')

    # Call OpenAI GPT-4 Vision API
    try:
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Please describe this image in detail. Focus on what you can clearly see - objects, people, animals, setting, colors, actions, etc. Be specific and accurate in your description."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500,
            temperature=0.1  # Low temperature for more consistent descriptions
        )
        
        # Extract the description
        description = response.choices[0].message.content.strip()
        return description
        
    except Exception as e:
        raise RuntimeError(f"OpenAI API error: {str(e)}")

class ImageAnalyzer(Agent):
    # satisfy Pydantic's required fields:
    role: str = "Image Analyzer"
    goal: str = "Describe in kid-friendly terms what is in the provided image using OpenAI's GPT-4 Vision model."
    backstory: str = (
        "You are a vision expert who uses OpenAI's GPT-4 Vision model to provide accurate and detailed image descriptions."
    )
    model_config = ConfigDict(extra="ignore")

    def handle(self, data: Any) -> Any:
        # Extract image path from the data
        image_path = data.get("image_path")
        if not image_path:
            return {"image_description": "No image provided"}
        
        # Use the OpenAI function to analyze the image
        description = analyze_image_with_openai(image_path)
        return {"image_description": description}
