from crewai import Task
import logging

logger = logging.getLogger(__name__)

class TaskValidator(Task):
    """Pass the researcher's output to the Validator agent."""
    def __init__(self, description, expected_output, agent=None):
        super().__init__(description=description, expected_output=expected_output, agent=agent)
    
    def run(self, data):
        logger.info(f"🔍 TaskValidator received data: {data}")
        result = {"content": data.get("content", "")}
        logger.info(f"🔍 TaskValidator returning: {result}")
        return result

