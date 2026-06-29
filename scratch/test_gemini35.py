import os
import time
from google import genai
from dotenv import load_dotenv

load_dotenv()

def test_model():
    api_key = os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=api_key)
    
    print("Testing gemini-3.5-flash:")
    start = time.time()
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents="Say hello and tell me your model name.",
        )
        elapsed = time.time() - start
        print(f"Success! Time taken: {elapsed:.2f} seconds")
        print(f"Response: {response.text.strip()}")
    except Exception as e:
        elapsed = time.time() - start
        print(f"Failed after {elapsed:.2f} seconds. Error: {e}")

if __name__ == "__main__":
    test_model()
