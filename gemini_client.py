import time

from google import genai
from google.genai import types

from config import GEMINI_API_KEY, GEMINI_MODEL


if not GEMINI_API_KEY:
    client = None
else:
    client = genai.Client(api_key=GEMINI_API_KEY)


def generate_content(prompt: str, temperature: float = 0.7) -> str:
    if client is None:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Please add your Gemini API key to the .env file."
        )

    last_error = None

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                ),
            )

            if not response.text:
                raise RuntimeError("Gemini returned an empty response.")

            return response.text.strip()

        except Exception as error:
            last_error = error

            if attempt < 2:
                time.sleep(2 * (attempt + 1))
            else:
                print("GEMINI ERROR:", repr(last_error))
                raise RuntimeError(
                f"Gemini service is temporarily unavailable. "
                f"Details: {last_error}"
                )