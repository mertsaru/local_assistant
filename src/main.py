from pydantic import BaseModel
import argparse
import os

import uvicorn
from fastapi import FastAPI

from src.chatbot import chatbot

parser = argparse.ArgumentParser(
    description="Local Assistant - An AI assistant that runs locally on your machine."
)
parser.add_argument("--dev", action="store_true", help="Run in development mode.")
args = parser.parse_args()

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


agentic_chatbot = chatbot.Chatbot()


@app.post("/chat")
async def chat(request: ChatRequest):
    response = await agentic_chatbot.generate_answer(request.message)
    return response


if args.dev:
    import asyncio

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        request = ChatRequest(message=user_input)
        response = asyncio.run(agentic_chatbot.generate_answer(request.message))

        print("Bot: ", response)
else:
    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "10102")),
        workers=int(os.getenv("WORKERS", "1")),
    )
