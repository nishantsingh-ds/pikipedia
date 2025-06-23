from crewai import Task
import logging

logger = logging.getLogger(__name__)

class TaskResearcher(Task):
    """Pass the user's topic and image description to the Researcher agent."""
    def __init__(self, description, expected_output, agent=None):
        super().__init__(description=description, expected_output=expected_output, agent=agent)
    
    def run(self, data):
        logger.info(f"🔍 TaskResearcher received data: {data}")
        result = {"topic": data.get("topic", "")}
        
        # Include image description if available
        if "image_description" in data:
            result["image_description"] = data.get("image_description", "")
        
        logger.info(f"🔍 TaskResearcher returning: {result}")
        return result
