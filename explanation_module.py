from config import (
    USE_LOCAL_EXPLAINER,
    LOCAL_EXPLAINER_MODEL,
)

from gemini_client import generate_content


_local_pipeline = None


def load_local_model():

    global _local_pipeline

    if _local_pipeline is not None:
        return _local_pipeline

    try:
        from transformers import pipeline

        _local_pipeline = pipeline(
            "text2text-generation",
            model=LOCAL_EXPLAINER_MODEL,
        )

        return _local_pipeline

    except Exception:
        return None


def explain_with_local_model(
    topic: str,
    level: str,
):

    model = load_local_model()

    if model is None:
        return None

    prompt = f"""
Explain the following topic to a {level} student.

Topic:
{topic}

Make the explanation simple, structured and educational.
"""

    result = model(
        prompt,
        max_new_tokens=400,
        do_sample=True,
    )

    if not result:
        return None

    return result[0]["generated_text"]


def explain_topic(
    topic: str,
    level: str = "beginner",
) -> str:

    if USE_LOCAL_EXPLAINER:

        local_result = explain_with_local_model(
            topic,
            level,
        )

        if local_result:
            return local_result

    prompt = f"""
You are EduGenie, an AI tutor.

Explain the topic below to a {level} learner.

Topic:
{topic}

Structure the explanation as:

1. Simple definition
2. Main idea
3. Step-by-step explanation
4. Example
5. Important points
6. Short recap

Use simple language and avoid unnecessary complexity.
"""

    return generate_content(prompt)