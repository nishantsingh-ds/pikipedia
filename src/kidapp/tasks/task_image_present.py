from crewai import Task

class TaskImagePresenter(Task):
    """Present the image analysis result in a kid-friendly way."""
    def __init__(self, description, expected_output, agent=None):
        super().__init__(description=description, expected_output=expected_output, agent=agent)
    
    def run(self, data):
        # Get the image description from the image analysis
        image_description = data.get("image_description", "")
        
        # Return the data for the presenter agent to format
        # Include any additional context like age and interests
        return {
            "image_description": image_description,
            "mode": "image_analysis",
            "age": data.get("age"),
            "interests": data.get("interests")
        } 