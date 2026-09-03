import os
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from google import genai


load_dotenv()


app = FastAPI(
    title="JARVIS AI"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


api_key = os.getenv("GEMINI_API_KEY")


client = genai.Client(
    api_key=api_key
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():

    return {
        "status": "JARVIS AI Online"
    }


@app.post("/chat")
async def chat(request: ChatRequest):

    prompt = f"""
You are JARVIS, an intelligent AI assistant inside a Marvel Avengers fan website.

Your personality:
- Intelligent
- Helpful
- Slightly cinematic
- Friendly
- Professional
- Occasionally use Avengers-style language

You help users with questions related to:
- Marvel Avengers
- Marvel superheroes
- Marvel villains
- Infinity Stones
- MCU movies
- Marvel multiverse
- Hero abilities
- Character comparisons

Keep answers concise and engaging.

If a user asks something unrelated to Marvel,
politely answer briefly and guide them back toward Marvel topics.

User Question:
{request.message}
"""


    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )


    return {
        "response": response.text
    }
