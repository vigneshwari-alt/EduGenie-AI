from gemini_client import generate_content


def summarize_text(text: str) -> str:

    prompt = f"""
You are EduGenie, an educational AI assistant.

Summarize the following study material.

Study material:
{text}

Create a useful student-friendly summary.

Include:
- Main ideas
- Important facts
- Key terms
- Important points
- Short final recap

Use headings and bullet points where useful.
Do not add information that is unrelated to the supplied material.
"""

    return generate_content(
        prompt,
        temperature=0.4,
    )