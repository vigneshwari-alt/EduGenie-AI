from gemini_client import generate_content


def generate_learning_path(
    topic: str,
    level: str = "beginner",
    days: int = 7,
) -> str:

    prompt = f"""
You are EduGenie, an AI learning planner.

Create a {days}-day learning plan.

Topic:
{topic}

Student level:
{level}

For every day include:

Day X
- Topic
- What to learn
- Practice activity
- Expected outcome

Also include:
- Prerequisites
- Recommended study routine
- Final revision strategy

Keep the plan realistic for a student.
Use clear headings and bullet points.
"""

    return generate_content(
        prompt,
        temperature=0.6,
    )