from pydantic import BaseModel

from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn

load_dotenv()

import config
from .chatbot import chatbot

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest): # TODO use await while using chatbot generate
    response = await chatbot.generate_answer(request.message)
    return response

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=11987,
        reload=False,
        log_level="info",
        workers=1,
    )
