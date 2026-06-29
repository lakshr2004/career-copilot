import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def list_models():
    api_key = os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=api_key)
    
    print("Listing models:")
    try:
        # Check if list models is available
        models = client.models.list()
        for m in models:
            print(f"Name: {m.name}, Supported Actions: {m.supported_actions}")
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    list_models()
