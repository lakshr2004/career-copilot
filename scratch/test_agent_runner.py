import os
import time
import asyncio
from pydantic import BaseModel, Field
from typing import List
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class TestSchema(BaseModel):
    skills: List[str]
    ats_score: int
    suggestions: List[str]

async def test_agent(model_name):
    print(f"\nTesting agent with model: {model_name}")
    agent = Agent(
        name="test_agent",
        model=model_name,
        instruction="Evaluate the candidate's skills and score them.",
        output_schema=TestSchema
    )
    
    runner = InMemoryRunner(agent=agent)
    runner.auto_create_session = True
    msg = types.Content(
        role="user",
        parts=[types.Part.from_text(text="Skills: Java, SQL. Seeking Dev role.")]
    )
    
    final_text = ""
    start = time.time()
    try:
        async for event in runner.run_async(user_id="student", session_id="test_session", new_message=msg):
            if event.message and event.message.parts:
                for part in event.message.parts:
                    if part.text:
                        final_text += part.text
            elif event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        final_text += part.text
        elapsed = time.time() - start
        print(f"Success! Agent took: {elapsed:.2f} seconds")
        print(f"Response: {final_text}")
    except Exception as e:
        elapsed = time.time() - start
        print(f"Failed after {elapsed:.2f} seconds. Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_agent("gemini-3.1-flash-lite"))
