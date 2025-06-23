from crewai import Task
import logging

logger = logging.getLogger(__name__)

class TaskPresenter(Task):
    """Pass the analogy, content, validation status, topic, and image description to the Presenter agent."""
    def __init__(self, description, expected_output, agent=None):
        super().__init__(description=description, expected_output=expected_output, agent=agent)
    
    def run(self, data):
        logger.info(f"🔍 TaskPresenter received data: {data}")
        result = {
            "analogy": data.get("analogy", ""),
            "content": data.get("content", ""),
            "status": data.get("status", ""),
            "notes": data.get("notes", ""),
            "topic": data.get("topic", "")
        }
        
        # Include image description if available
        if "image_description" in data:
            result["image_description"] = data.get("image_description", "")
        
        logger.info(f"🔍 TaskPresenter returning: {result}")
        return result 