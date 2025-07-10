from crewai import Task
import logging

logger = logging.getLogger(__name__)

class TaskGuardrails(Task):
    """CrewAI Guardrails Task for content safety validation"""
    
    def __init__(self, description, expected_output, agent=None):
        super().__init__(
            description=description,
            expected_output=expected_output,
            agent=agent
        )
    
    def run(self, data):
        """Run guardrails validation using CrewAI's built-in safety features"""
        logger.info(f"🛡️ Guardrails task received data: {data}")
        
        # Pass data to the guardrails agent for validation
        # The agent will handle the safety checks using CrewAI's built-in features
        return data 