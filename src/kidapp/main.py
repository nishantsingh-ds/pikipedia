#!/usr/bin/env python
import os, warnings
from pathlib import Path
from gtts import gTTS
from kidapp.crew import KidSafeAppCrew  # your Crew class

# point CrewAI at your config directory
BASE = Path(__file__).parent
os.environ["CREW_CONFIG"] = str(BASE / "config")

warnings.filterwarnings("ignore", category=SyntaxWarning)

def get_image_path():
    path = input("\n(Optional) Enter image file path (or leave blank): ").strip()
    return path or None

def get_topic():
    topic = ""
    while not topic:
        topic = input("\nEnter topic/question: ").strip()
    return topic

def text_to_speech(text, filename="response.mp3"):
    out = BASE / filename
    gTTS(text=text, lang="en").save(str(out))
    return out

def run():
    # 1) instantiate the Crew
    crew = KidSafeAppCrew().crew()

    # 2) collect inputs
    inputs = {}
    img_path = get_image_path()
    if img_path:
        inputs["image_path"] = img_path

    topic = get_topic()
    inputs["topic"] = topic

    # 3) kick off the entire pipeline in one shot:
    #    it will execute in order: image_analysis_task -> research_task -> validate_task ->
    #    analogy_task -> present_task, using the inputs dict.
    crew.kickoff(inputs=inputs)
    
if __name__ == "__main__":
    run()
