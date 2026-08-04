import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_sql(prompt: str):
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite", # gemini-flash-latest
        contents=prompt,
    )

    return response.text.strip()