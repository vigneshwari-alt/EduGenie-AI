from fastapi import FastAPI, Request, HTTPException
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from config import APP_NAME
from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import generate_learning_path


app = FastAPI(
    title=APP_NAME,
    description="Gemini-powered AI Learning Assistant",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


# -----------------------------
# Request Models
# -----------------------------

class QARequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=5000)


class ExplanationRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=5000)
    level: str = "beginner"


class QuizRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=5000)
    num_questions: int = Field(default=5, ge=1, le=10)
    level: str = "beginner"


class SummaryRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=15000)


class LearningPathRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=5000)
    level: str = "beginner"
    days: int = Field(default=7, ge=1, le=30)


# -----------------------------
# Frontend
# -----------------------------

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "app_name": APP_NAME
        },
    )

# -----------------------------
# Health Check
# -----------------------------

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "app": APP_NAME,
    }


# -----------------------------
# Q&A
# -----------------------------

@app.post("/qa")
async def qa(request: QARequest):
    try:
        answer = answer_question(request.question)

        return {
            "success": True,
            "question": request.question,
            "answer": answer,
        }

    except Exception as e:
        error_message = str(e)

        if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message or "quota" in error_message.lower():
            raise HTTPException(
                status_code=429,
                detail="Gemini API quota exceeded. Please wait for the quota to reset and try again."
            )

        raise HTTPException(
            status_code=500,
            detail="Gemini service is temporarily unavailable. Please try again later."
        )


# -----------------------------
# Explanation
# -----------------------------

@app.post("/explain")
async def explain(request: ExplanationRequest):
    explanation = explain_topic(
        request.topic,
        request.level,
    )

    return {
        "success": True,
        "topic": request.topic,
        "level": request.level,
        "explanation": explanation,
    }


# -----------------------------
# Quiz
# -----------------------------

@app.post("/quiz")
async def quiz(request: QuizRequest):
    quiz = generate_quiz(
        request.topic,
        request.num_questions,
        request.level,
    )

    return {
        "success": True,
        "quiz": quiz,
    }


# -----------------------------
# Summarization
# -----------------------------

@app.post("/summarize")
async def summarize(request: SummaryRequest):
    summary = summarize_text(request.text)

    return {
        "success": True,
        "summary": summary,
    }


# -----------------------------
# Learning Path
# -----------------------------

@app.post("/learn/recommendations")
async def learning_path(request: LearningPathRequest):
    plan = generate_learning_path(
        request.topic,
        request.level,
        request.days,
    )

    return {
        "success": True,
        "plan": plan,
    }