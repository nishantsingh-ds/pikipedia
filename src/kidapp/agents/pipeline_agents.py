"""
Collaborative agent pipeline for KidApp.
Each agent takes and updates the context dict.
"""

def researcher_agent(context):
    topic = context.get("topic")
    age = context.get("age")
    interests = context.get("interests")
    # For now, just echo the topic as a 'fact'.
    context["facts"] = f"Facts about '{topic}' for age {age} and interests {interests}."
    return context

def explainer_agent(context):
    facts = context.get("facts")
    age = context.get("age")
    # Simplify facts for kids (stub)
    context["explanation"] = f"Explained for kids: {facts}"
    return context

def fact_checker_agent(context):
    explanation = context.get("explanation")
    # Assume explanation is always correct (stub)
    context["fact_checked"] = True
    return context

def analogy_agent(context):
    explanation = context.get("explanation")
    # Add a fun analogy (stub)
    context["analogy"] = f"It's like a fun game! ({explanation})"
    return context

def quiz_agent(context):
    explanation = context.get("explanation")
    # Generate a simple quiz (stub)
    context["quiz"] = [
        {"question": f"What did you learn about {context.get('topic')}?", "answer": explanation}
    ]
    return context

def diagram_agent(context):
    # Stub: return a placeholder image URL
    context["diagram_url"] = "https://placehold.co/400x300?text=Diagram+Coming+Soon"
    return context

def audio_agent(context):
    # Stub: return a placeholder audio URL
    context["audio_url"] = "https://placehold.co/1s.mp3?text=Audio+Coming+Soon"
    return context

def run_pipeline(context):
    context = researcher_agent(context)
    context = explainer_agent(context)
    context = fact_checker_agent(context)
    context = analogy_agent(context)
    context = quiz_agent(context)
    context = diagram_agent(context)
    context = audio_agent(context)
    return context 