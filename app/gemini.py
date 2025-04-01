import os
import httpx
import json
from dotenv import load_dotenv

load_dotenv()

# API_KEY = os.getenv("GEMINI_API_KEY")
API_KEY = "AIzaSyAp_zaLyYW5BA-ZCj2YZ3AcOMtvjAJ1mTg"

print(API_KEY)

URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

def load_system_prompt() -> str:
    prompt_path = os.path.join(os.path.dirname(__file__), "utils", "system_prompt.json")
    with open(prompt_path, "r") as f:
        data = json.load(f)
        return f"{data['requirements']}\n\n{data['boundries']}\n\nNow, answer the following question:\n\n"

SYSTEM_PROMPT = load_system_prompt()

async def get_gemini_response(prompt: str) -> str:
    full_prompt = SYSTEM_PROMPT + prompt
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": full_prompt}]
            }
        ]
    }

    timeout = httpx.Timeout(20.0, connect=5.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(URL, json=payload)
        data = response.json()
        print("Gemini raw response:", data)  # Optional: for debugging

        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            return "Sorry, I couldn't process that."
