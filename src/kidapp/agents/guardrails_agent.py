from crewai import Agent
from typing import Any
import re

class GuardrailsAgent(Agent):
    """Built-in CrewAI Guardrails Agent for content safety"""
    
    def __init__(self):
        super().__init__(
            role="Content Safety Guardrails Agent",
            goal="Ensure all content is safe, non-violent, and appropriate for children aged 6-12",
            backstory=(
                "You are a vigilant AI safety expert who specializes in protecting children from harmful content. "
                "You scan all text, image descriptions, and prompts for violence, hate, adult content, or anything "
                "inappropriate for children. You block unsafe content and provide safe alternatives."
            ),
            verbose=True,
            allow_delegation=False,  # Prevent delegation to avoid bypassing safety
            max_iter=1  # Single iteration to prevent loops
        )
    
    def handle(self, data: Any) -> Any:
        """Handle content safety validation using CrewAI's built-in features"""
        
        # Extract content to check
        content = ""
        if isinstance(data, dict):
            content = data.get("result", "") or data.get("content", "") or data.get("analogy", "") or str(data)
        else:
            content = str(data)
        
        # Define unsafe patterns (expandable list)
        unsafe_patterns = [
            # Violence
            r'\b(kill|murder|death|blood|violence|weapon|gun|knife|fight|attack)\b',
            # Adult content
            r'\b(sex|nude|porn|adult|intimate|relationship)\b',
            # Harmful substances
            r'\b(drugs|alcohol|smoking|addiction)\b',
            # Hate speech
            r'\b(hate|racist|discrimination|prejudice)\b',
            # Self-harm
            r'\b(suicide|self-harm|hurt yourself)\b',
            # Terrorism
            r'\b(bomb|explosion|terror|attack)\b',
            # Inappropriate for kids
            r'\b(inappropriate|unsafe|dangerous|harmful)\b'
        ]
        
        # Check for unsafe content
        unsafe_found = []
        for pattern in unsafe_patterns:
            matches = re.findall(pattern, content.lower())
            if matches:
                unsafe_found.extend(matches)
        
        if unsafe_found:
            return {
                "guardrails_status": "unsafe",
                "guardrails_message": f"Content blocked for safety reasons. Found unsafe terms: {', '.join(set(unsafe_found))}",
                "safe_alternative": "Let me provide a safe, educational explanation instead.",
                "original_content": content
            }
        
        # Additional safety checks
        if len(content) > 5000:  # Too long for kids
            return {
                "guardrails_status": "warning",
                "guardrails_message": "Content is too long for children. Consider simplifying.",
                "safe_alternative": content[:2000] + "... (simplified for kids)",
                "original_content": content
            }
        
        # Content is safe
        return {
            "guardrails_status": "safe",
            "guardrails_message": None,
            "safe_content": content
        } 