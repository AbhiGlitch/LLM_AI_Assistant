from fastapi import FastAPI
import os
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing. Check your .env file.")

client = genai.Client(api_key=api_key)
conversation_history = []
class Question(BaseModel):
    text: str

app = FastAPI()

@app.get("/")
def home():
    return {"message": "LLM AI Assistant API is running."}


@app.post("/ask")
def ask_question(question: Question):
    try:
        conversation_history.append(
            genai.types.Content(
                role="user",
                parts=[genai.types.Part.from_text(text=question.text)]
            )
        )

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=conversation_history
        )

        conversation_history.append(
            genai.types.Content(
                role="model",
                parts=[genai.types.Part.from_text(text=response.text)]
            )
        )

        return {"response": response.text}

    except Exception as e:
        return {"error": str(e)}
