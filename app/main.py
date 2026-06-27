from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.model import generate_text, get_generator


class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=500)
    max_new_tokens: int = Field(default=50, ge=1, le=200)


class GenerateResponse(BaseModel):
    prompt: str
    generated_text: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_generator()
    yield


app = FastAPI(title="Small LLM API", version="0.1.0", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest):
    text = generate_text(request.prompt, max_new_tokens=request.max_new_tokens)
    return GenerateResponse(prompt=request.prompt, generated_text=text)
