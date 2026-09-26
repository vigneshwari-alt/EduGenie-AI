import os
from dotenv import load_dotenv


load_dotenv()


APP_NAME = os.getenv("APP_NAME", "EduGenie")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
)

USE_LOCAL_EXPLAINER = (
    os.getenv("USE_LOCAL_EXPLAINER", "false").lower() == "true"
)

LOCAL_EXPLAINER_MODEL = os.getenv(
    "LOCAL_EXPLAINER_MODEL",
    "MBZUAI/LaMini-Flan-T5-783M"
)

REQUEST_TIMEOUT_SECONDS = int(
    os.getenv("REQUEST_TIMEOUT_SECONDS", "60")
)