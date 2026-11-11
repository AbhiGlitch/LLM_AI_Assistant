import os
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing. Check your .env file.")

client = genai.Client(api_key=api_key)

conversation_history = []

def get_user_input():
    user_question = input("Enter your question: ").strip()
    if not user_question:
        print("Please enter a question.")
        return None
    return user_question

while True:
    user_question = get_user_input()

    if user_question is None:
        continue

    if user_question.lower() == "exit":
        print("Exiting the program.")
        break

    conversation_history.append(
        types.Content(
            role = "user",
            parts=[types.Part.from_text(text=user_question)]
        )
       )

    try:
        response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=conversation_history
        )
        return response.text

        conversation_history.append(
                types.Content(
                    role="model",
                    parts=[types.Part.from_text(text=response.text)]
                )
            )


        print(response.text)

    except Exception as e:
        print(f"Something went wrong: {e}")
        return None

