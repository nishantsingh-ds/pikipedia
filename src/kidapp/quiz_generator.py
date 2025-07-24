"""
Quiz generation system for WonderBot
"""

import uuid
from datetime import datetime
from typing import List, Dict, Any
from openai import OpenAI
import os
import json

from .models import Quiz, QuizQuestion, QuestionType, DifficultyLevel

def generate_quiz_from_explanation(
    explanation: str, 
    topic: str, 
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM,
    num_questions: int = 5
) -> Quiz:
    """Generate a quiz from an explanation using OpenAI."""
    
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OpenAI API key not configured")
    
    client = OpenAI(api_key=openai_api_key)
    
    # Create prompt for quiz generation
    prompt = f"""
    Create a {difficulty.value} level quiz about this topic: "{topic}"
    
    Based on this explanation:
    {explanation}
    
    Generate {num_questions} questions with the following requirements:
    1. Mix of question types: multiple choice, true/false, fill-in-the-blank
    2. Age-appropriate for children 6-12 years old
    3. Clear, simple language
    4. Include explanations for correct answers
    5. Make it fun and engaging
    
    Return the quiz as a JSON object with this structure:
    {{
        "title": "Quiz title",
        "questions": [
            {{
                "question": "Question text",
                "question_type": "multiple_choice|true_false|fill_blank",
                "correct_answer": "Correct answer",
                "options": ["Option A", "Option B", "Option C", "Option D"], // for multiple choice
                "explanation": "Why this answer is correct"
            }}
        ]
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            temperature=0.7
        )
        
        content = response.choices[0].message.content.strip()
        
        # Parse JSON response
        try:
            quiz_data = json.loads(content)
        except json.JSONDecodeError:
            # Fallback: create a simple quiz
            quiz_data = create_fallback_quiz(topic, explanation)
        
        # Convert to Quiz model
        questions = []
        for q_data in quiz_data.get("questions", []):
            question = QuizQuestion(
                question=q_data.get("question", ""),
                question_type=QuestionType(q_data.get("question_type", "multiple_choice")),
                correct_answer=q_data.get("correct_answer", ""),
                options=q_data.get("options"),
                explanation=q_data.get("explanation"),
                difficulty=difficulty
            )
            questions.append(question)
        
        quiz = Quiz(
            id=str(uuid.uuid4()),
            title=quiz_data.get("title", f"Quiz about {topic}"),
            topic=topic,
            questions=questions,
            difficulty=difficulty,
            estimated_time=len(questions) * 2  # 2 minutes per question
        )
        
        return quiz
        
    except Exception as e:
        # Fallback quiz generation
        return create_fallback_quiz(topic, explanation, difficulty)

def create_fallback_quiz(topic: str, explanation: str, difficulty: DifficultyLevel = DifficultyLevel.MEDIUM) -> Quiz:
    """Create a simple fallback quiz if AI generation fails."""
    
    questions = [
        QuizQuestion(
            question=f"What is the main topic of this lesson?",
            question_type=QuestionType.MULTIPLE_CHOICE,
            correct_answer=topic,
            options=[topic, "Something else", "I don't know", "Maybe"],
            explanation=f"The main topic is {topic}",
            difficulty=difficulty
        ),
        QuizQuestion(
            question=f"True or False: This lesson teaches us something interesting.",
            question_type=QuestionType.TRUE_FALSE,
            correct_answer="True",
            explanation="This lesson is designed to be interesting and educational",
            difficulty=difficulty
        ),
        QuizQuestion(
            question=f"Fill in the blank: This lesson is about _____.",
            question_type=QuestionType.FILL_BLANK,
            correct_answer=topic,
            explanation=f"The lesson is about {topic}",
            difficulty=difficulty
        )
    ]
    
    return Quiz(
        id=str(uuid.uuid4()),
        title=f"Quick Quiz about {topic}",
        topic=topic,
        questions=questions,
        difficulty=difficulty,
        estimated_time=6
    )

def save_quiz_to_memory(quiz: Quiz) -> None:
    """Save quiz to memory storage."""
    from .models import memory_storage
    memory_storage.quizzes[quiz.id] = quiz

def get_quiz_by_id(quiz_id: str) -> Quiz:
    """Get a quiz by ID from memory storage."""
    from .models import memory_storage
    return memory_storage.quizzes.get(quiz_id)

def get_quizzes_by_topic(topic: str) -> List[Quiz]:
    """Get all quizzes for a specific topic."""
    from .models import memory_storage
    return [quiz for quiz in memory_storage.quizzes.values() if quiz.topic.lower() == topic.lower()]

def submit_quiz_attempt(quiz_id: str, user_id: str, answers: Dict[str, str]) -> Dict[str, Any]:
    """Submit a quiz attempt and calculate score."""
    quiz = get_quiz_by_id(quiz_id)
    if not quiz:
        raise ValueError("Quiz not found")
    
    # Calculate score
    correct_answers = 0
    total_questions = len(quiz.questions)
    
    for i, question in enumerate(quiz.questions):
        question_id = str(i)
        user_answer = answers.get(question_id, "")
        
        if question.question_type == QuestionType.TRUE_FALSE:
            if user_answer.lower() == question.correct_answer.lower():
                correct_answers += 1
        elif question.question_type == QuestionType.MULTIPLE_CHOICE:
            if user_answer == question.correct_answer:
                correct_answers += 1
        elif question.question_type == QuestionType.FILL_BLANK:
            if user_answer.lower().strip() == question.correct_answer.lower().strip():
                correct_answers += 1
        elif question.question_type == QuestionType.SHORT_ANSWER:
            # Simple keyword matching for short answers
            if any(keyword in user_answer.lower() for keyword in question.correct_answer.lower().split()):
                correct_answers += 1
    
    score = (correct_answers / total_questions) * 100
    
    # Create quiz attempt
    from .models import QuizAttempt, memory_storage
    attempt = QuizAttempt(
        quiz_id=quiz_id,
        user_id=user_id,
        score=score,
        total_questions=total_questions,
        correct_answers=correct_answers,
        time_taken=0,  # TODO: Track actual time
        answers=answers
    )
    
    # Save attempt
    if user_id not in memory_storage.quiz_attempts:
        memory_storage.quiz_attempts[user_id] = []
    memory_storage.quiz_attempts[user_id].append(attempt)
    
    return {
        "score": score,
        "correct_answers": correct_answers,
        "total_questions": total_questions,
        "feedback": generate_feedback(score, quiz.difficulty),
        "attempt_id": str(uuid.uuid4())
    }

def generate_feedback(score: float, difficulty: DifficultyLevel) -> str:
    """Generate feedback based on quiz score."""
    if score >= 90:
        return f"🎉 Amazing! You're a {difficulty.value} level expert!"
    elif score >= 80:
        return f"🌟 Great job! You really understand this {difficulty.value} material!"
    elif score >= 70:
        return f"👍 Good work! You're getting the hang of this {difficulty.value} topic!"
    elif score >= 60:
        return f"📚 Keep practicing! This {difficulty.value} material takes time to master."
    else:
        return f"💪 Don't worry! {difficulty.value} level topics can be challenging. Try again!" 