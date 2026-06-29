import os
import time
from pydantic import BaseModel, Field
from typing import List
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class TestSchema(BaseModel):
    skills: List[str]
    score: int
    summary: str

def test_structured_model(model_name):
    api_key = os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=api_key)
    
    print(f"\nTesting structured output for model: {model_name}")
    start = time.time()
    try:
        response = client.models.generate_content(
            model=model_name,
            contents="Analyze a candidate with Python and SQL skills. Score them and write a summary.",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=TestSchema,
                temperature=0.2,
            )
        )
        elapsed = time.time() - start
        print(f"Success! Time taken: {elapsed:.2f} seconds")
        print(f"Response: {response.text.strip()}")
    except Exception as e:
        elapsed = time.time() - start
        print(f"Failed after {elapsed:.2f} seconds. Error: {e}")

if __name__ == "__main__":
    models = ["gemini-3.1-flash-lite", "gemini-2.5-flash-lite", "gemini-3-flash-preview"]
    for m in models:
        test_structured_model(m)
