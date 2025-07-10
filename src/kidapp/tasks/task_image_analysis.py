from crewai import Task

class TaskImageAnalysis(Task):
    """Analyzes the uploaded image using OpenAI's GPT-4 Vision model and returns a detailed description."""

    def __init__(self, description, expected_output, agent=None):
        super().__init__(description=description, expected_output=expected_output, agent=agent)

    def run(self, data):
        # Extract image path from the data
        image_path = data.get("image_path")
        if not image_path:
            return {"image_description": "No image provided"}
        
        # Pass the image path to the agent for analysis
        # The agent will handle the actual OpenAI Vision API call
        return {"image_path": image_path}
