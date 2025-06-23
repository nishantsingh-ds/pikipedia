from crewai import Task
import logging

logger = logging.getLogger(__name__)

class TaskAnaloger(Task):
    """Pass the validated content, original topic, and image description to the Analoger agent."""
    def __init__(self, description, expected_output, agent=None):
        super().__init__(description=description, expected_output=expected_output, agent=agent)
    
    def run(self, data):
        logger.info(f"🔍 TaskAnaloger received data: {data}")
        result = {
            "content": data.get("content", ""),
            "topic": data.get("topic", "")
        }
        
        # Include image description if available
        if "image_description" in data:
            result["image_description"] = data.get("image_description", "")
        
        logger.info(f"🔍 TaskAnaloger returning: {result}")
        return result
