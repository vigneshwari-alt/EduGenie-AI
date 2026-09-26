import json
import re

from gemini_client import generate_content


def extract_json(text: str):

    text = text.strip()

    # Remove markdown code fences
    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"^```\s*",
        "",
        text,
    )

    text = re.sub(
        r"\s*```$",
        "",
        text,
    )

    # Try direct parsing
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Find JSON object
    object_match = re.search(
        r"\{.*\}",
        text,
        flags=re.DOTALL,
    )

    if object_match:
        try:
            return json.loads(
                object_match.group(0)
            )
        except json.JSONDecodeError:
            pass

    # Find JSON array
    array_match = re.search(
        r"\[.*\]",
        text,
        flags=re.DOTALL,
    )

    if array_match:
        try:
            return json.loads(
                array_match.group(0)
            )
        except json.JSONDecodeError:
            pass

    raise ValueError(
        "Gemini did not return valid JSON."
    )


def normalize_quiz(data, topic: str):

    if isinstance(data, dict):

        questions = data.get(
            "questions",
            data.get("quiz", [])
        )

    elif isinstance(data, list):

        questions = data

    else:

        questions = []

    normalized = []

    for index, question in enumerate(
        questions,
        start=1
    ):

        if not isinstance(question, dict):
            continue

        q_text = question.get(
            "question",
            question.get("text", "")
        )

        options = question.get(
            "options",
            []
        )

        answer = question.get(
            "answer",
            question.get(
                "correct_answer",
                ""
            )
        )

        explanation = question.get(
            "explanation",
            ""
        )

        if not q_text:
            continue

        normalized.append(
            {
                "id": index,
                "question": q_text,
                "options": options,
                "answer": answer,
                "explanation": explanation,
            }
        )

    return {
        "topic": topic,
        "questions": normalized,
    }


def generate_quiz(
    topic: str,
    num_questions: int = 5,
    level: str = "beginner",
):

    prompt = f"""
Create a multiple-choice educational quiz.

Topic:
{topic}

Student level:
{level}

Number of questions:
{num_questions}

Return ONLY valid JSON.

Use exactly this structure:

{{
  "questions": [
    {{
      "question": "Question text",
      "options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "answer": "The exact correct option text",
      "explanation": "Short explanation of why it is correct"
    }}
  ]
}}

Requirements:
- Exactly {num_questions} questions.
- Four options per question.
- Exactly one correct answer.
- Do not use markdown.
- Keep questions educational and relevant.
"""

    raw = generate_content(
        prompt,
        temperature=0.5,
    )

    try:

        data = extract_json(raw)

    except ValueError:

        repair_prompt = f"""
Convert the following quiz into valid JSON.

Return ONLY JSON using this exact structure:

{{
  "questions": [
    {{
      "question": "Question",
      "options": [
        "A",
        "B",
        "C",
        "D"
      ],
      "answer": "Correct option",
      "explanation": "Explanation"
    }}
  ]
}}

Quiz:
{raw}
"""

        repaired = generate_content(
            repair_prompt,
            temperature=0.1,
        )

        data = extract_json(repaired)

    return normalize_quiz(
        data,
        topic,
    )