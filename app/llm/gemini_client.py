import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

MODEL_NAME = os.getenv("GEMINI_MODEL")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_sql(prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

        sql = getattr(response, "text", "")

        if not sql:
            raise RuntimeError("Gemini returned an empty response.")

        return sql.strip()

    except Exception as e:
        raise RuntimeError(f"Failed to generate SQL: {e}")