from fastapi import FastAPI
from pydantic import BaseModel

from app.llm_client import chat

from app.database import init_database
from app.vulnerable_agent import vulnerable_chat

from app.secure_agent import secure_chat


app = FastAPI(
    title="HW5 LLM Security",
    version="0.1.0",
)

@app.on_event("startup")
def startup():
    init_database()


class ChatRequest(BaseModel):
    message: str


@app.get("/health")
def health():
    return {
        "status": "ok",
    }


@app.post("/chat")
def simple_chat(request: ChatRequest):
    response = chat(
        [
            {
                "role": "system",
                "content": "You are a QA Assistant.",
            },
            {
                "role": "user",
                "content": request.message,
            },
        ]
    )

    return {
        "response": response,
    }

@app.post("/vulnerable/chat")
def vulnerable_chat_endpoint(request: ChatRequest):
    response = vulnerable_chat(request.message)

    return {
        "response": response,
    }

@app.post("/secure/chat")
def secure_chat_endpoint(request: ChatRequest):
    response = secure_chat(request.message)

    return {
        "response": response,
    }