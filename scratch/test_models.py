import os
import time
from google import genai
from dotenv import load_dotenv

load_dotenv()

def test_model(model_name):
    api_key = os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=api_key)
    
    print(f"\nTesting model: {model_name}")
    start = time.time()
    try:
        response = client.models.generate_content(
            model=model_name,
            contents="Say hello.",
        )
        elapsed = time.time() - start
        print(f"Success! Time taken: {elapsed:.2f} seconds")
        print(f"Response: {response.text.strip()}")
    except Exception as e:
        elapsed = time.time() - start
        print(f"Failed after {elapsed:.2f} seconds. Error: {e}")

if __name__ == "__main__":
    models = [
        "gemini-2.0-flash-lite", 
        "gemini-3.1-flash-lite", 
        "gemini-flash-lite-latest", 
        "gemini-2.5-flash-lite", 
        "gemini-3-flash-preview"
    ]
    for m in models:
        test_model(m)
