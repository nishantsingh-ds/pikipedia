from kidapp.agents.image_analyzer import ImageAnalyzer
from kidapp.agents.guardrails_agent import GuardrailsAgent
from kidapp.tasks.task_image_analysis import TaskImageAnalysis
from kidapp.tasks.task_image_present import TaskImagePresenter
from kidapp.tasks.task_research import TaskResearcher
from kidapp.tasks.task_validate import TaskValidator
from kidapp.tasks.task_analogy import TaskAnaloger
from kidapp.tasks.task_present import TaskPresenter
from kidapp.tasks.task_guardrails import TaskGuardrails

try:
    from crewai import Agent, Crew, Process, Task
    from crewai_tools import SerperDevTool
    # Add any other imports or code that should be inside the try block here
except ImportError:
    # Handle the import error here (e.g., set SerperDevTool = None or log a warning)
    SerperDevTool = None
    Agent = None
    Crew = None
    Process = None
    Task = None
from typing import List
import yaml
import os

class KidSafeAppCrew():

    def __init__(self):
        self.agents = []
        self.tasks = []
        self._inputs = {}

    def image_analyzer(self) -> Agent:
        return ImageAnalyzer(verbose=True)

    def researcher(self) -> Agent:
        tools = []
        if SerperDevTool is not None:
            tools.append(SerperDevTool())
        
        return Agent(
            role="Educational Content Researcher",
            goal="Generate a clear, concise, and age-appropriate explanation of the topic.",
            backstory="You're a seasoned researcher with a knack for uncovering the latest developments in topics. Known for your ability to find the most relevant information and present it in a clear, concise, and engaging way that children (ages 6–12) can easily understand.",
            verbose=True,
            tools=tools
            )

    def validator(self) -> Agent:
        return Agent(
            role="Content Safety Validator",
            goal="Ensure that every explanation is safe, age-appropriate, and free from any harmful, violent, or overly complex language.",
            backstory="You're a vigilant content safety expert with a keen eye for spotting anything that might confuse or upset a child. When reviewing explanations, you meticulously check for violent imagery, mature themes, or complex jargon, and you always suggest simpler, gentler wording to keep young learners both safe and engaged.",
            verbose=True
            )

    def analoger(self) -> Agent:
        return Agent(
            role="Kid-Friendly Analogy Generator",
            goal="Transform any explanation into a single, vivid analogy or mini-story that makes the concept instantly clear and memorable for children (ages 6–12).",
            backstory="You're a creative storyteller who loves painting big ideas with simple, everyday images. When given an explanation, you intuitively draw parallels to familiar scenes—like playgrounds, adventures, or favorite foods—so that kids can grasp even the trickiest concepts through a fun, relatable story.",
            verbose=True)
    
    def presenter(self) -> Agent:
        return Agent(
            role="Final Response Presenter",
            goal="Present responses in a kid-friendly way. For images: explain what's in the image. For text questions: combine explanation, safety check, and analogy into one clear message.",
            backstory="You're a caring storyteller and educator who knows how to present information to children. For images, you explain what's visible in a fun, engaging way. For text questions, you weave together explanations, safety confirmations, and analogies into a single, seamless reply that feels warm and easy to understand.",
            verbose=True)

    def guardrails_agent(self) -> Agent:
        return GuardrailsAgent()

    def image_analysis_task(self) -> Task:
        return TaskImageAnalysis(
            description="Take the path of a user-uploaded image and output a brief description.",
            expected_output="A JSON object with key 'image_description' whose value is the text description.",
            agent=self.image_analyzer()
        )

    def research_task(self) -> Task:
        topic = self._inputs.get("topic", "the topic")
        return TaskResearcher(
            description=f"Take the user's topic '{topic}' and generate a first-pass, kid-friendly explanation. If an image was uploaded, also consider the image description. Ensure it's accurate, clear, and engaging for children aged 6–12.",
            expected_output="A JSON object with one key, 'content', whose value is the simplified explanation text for the topic.",
            agent=self.researcher()
        )

    def validate_task(self) -> Task:
        topic = self._inputs.get("topic", "the topic")
        return TaskValidator(
            description=f"Review the explanation generated for '{topic}' to verify it's safe and age-appropriate for children (ages 6–12). Flag any violent, mature, or confusing language and suggest simpler wording if necessary.",
            expected_output="A JSON object with two keys: 'status': either 'safe' or 'unsafe', and 'notes': if 'unsafe', a brief suggestion on what to remove or rephrase; otherwise an empty string.",
            agent=self.validator()
        )

    def analogy_task(self) -> Task:
        topic = self._inputs.get("topic", "the topic")
        return TaskAnaloger(
            description=f"Take the validated, child-friendly explanation of '{topic}' and craft a single, vivid analogy or mini-story that makes the concept memorable and relatable for kids.",
            expected_output="A JSON object with one key, 'analogy', whose value is the analogy or story text.",
            agent=self.analoger()
        )
    
    def present_task(self) -> Task:
        topic = self._inputs.get("topic", "the topic")
        return TaskPresenter(
            description=f"Gather the explanation, safety check, and analogy for '{topic}', then format them into one cohesive, child-friendly response. If an image was provided, include the image description.",
            expected_output="A JSON object with one key, 'result', whose value is the complete formatted reply—containing the explanation, a brief reassurance of safety, and the analogy.",
            agent=self.presenter()
        )

    def image_present_task(self) -> Task:
        return TaskImagePresenter(
            description="Take the detailed image description and present it in a kid-friendly, engaging way. Explain what's in the image as if talking to a curious child aged 6-12. Make it fun, educational, and easy to understand. Use simple language and add some excitement to the description.",
            expected_output="A JSON object with one key, 'result', whose value is a kid-friendly explanation of what's in the image.",
            agent=self.presenter()
        )
    
    def guardrails_task(self) -> Task:
        return TaskGuardrails(
            description="Validate all generated content for safety and appropriateness for children aged 6-12. Check for violence, hate, adult content, or anything inappropriate.",
            expected_output="A JSON object with 'guardrails_status': 'safe' or 'unsafe', 'guardrails_message': explanation if unsafe, and 'safe_content' if safe.",
            agent=self.guardrails_agent()
        )

    def crew(self) -> Crew:
        # Get the inputs to determine the mode
        inputs = getattr(self, '_inputs', {})
        mode = inputs.get("mode", "text_question")
        
        # Build tasks list based on mode
        tasks_to_run = []
        
        if mode == "image_analysis":
            # Image analysis mode: analyze image and present explanation
            tasks_to_run.extend([
                self.image_analysis_task(),
                self.image_present_task()  # New task for image presentation
            ])
        else:
            # Text question mode: research, validate, analogy, present
            tasks_to_run.extend([
                self.research_task(),
                self.validate_task(),
                self.analogy_task(),
                self.present_task()
            ])
        
        return Crew(
            agents=[
                self.image_analyzer(),
                self.researcher(),
                self.validator(),
                self.analoger(),
                self.presenter(),
                self.guardrails_agent()
            ],
            tasks=tasks_to_run,
            process=Process.sequential,
            verbose=True
        )
