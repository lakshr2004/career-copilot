import os
from pydantic import BaseModel, Field
from typing import List
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class TechnicalQuestion(BaseModel):
    question: str = Field(description="The technical or coding question")
    topic: str = Field(description="The category (e.g. Data Structures, System Design, SQL, OOPs)")
    tips: str = Field(description="Key concepts or hints to solve this question")

class HRQuestion(BaseModel):
    question: str = Field(description="The behavioral or HR question")
    rationale: str = Field(description="What the recruiter is evaluating in this answer")
    strategy: str = Field(description="Answer structure guideline (e.g. using the STAR method)")

class StudyDay(BaseModel):
    day: str = Field(description="Timeframe indicator (e.g. 'Day 1', 'Day 2-3')")
    focus: str = Field(description="Primary topic of study")
    tasks: List[str] = Field(description="List of specific execution tasks/problems to solve")

class InterviewPrepResult(BaseModel):
    technical_questions: List[TechnicalQuestion]
    hr_questions: List[HRQuestion]
    study_plan: List[StudyDay]

def generate_prep_plan(resume_text: str, target_role: str) -> InterviewPrepResult:
    """
    Generates placement prep resources based on the candidate's profile and target role.
    """
    if not resume_text or not target_role:
        return InterviewPrepResult(
            technical_questions=[
                TechnicalQuestion(question="Sample: Explain polymorphism in Java.", topic="OOPs", tips="Use code example")
            ],
            hr_questions=[
                HRQuestion(question="Sample: Why do you want to join our company?", rationale="Check alignment", strategy="Mention company values")
            ],
            study_plan=[
                StudyDay(day="Day 1", focus="Basics", tasks=["Review programming fundamentals"])
            ]
        )

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return InterviewPrepResult(
            technical_questions=[],
            hr_questions=[],
            study_plan=[]
        )

    try:
        client = genai.Client(api_key=api_key)
        
        prompt = (
            f"You are a technical interview coach specializing in campus placements in India.\n"
            f"Provide custom prep material for a student aiming for the role of '{target_role}'.\n"
            f"Take into account their profile summary and skills.\n\n"
            f"--- STUDENT PROFILE/RESUME ---\n{resume_text}\n\n"
            f"Provide interview prep resources. Target top companies recruiting in India (e.g. TCS, Infosys, Microsoft, Amazon, Google, Flipkart).\n"
            f"Generate technical questions (DSA, System Design, DB, etc.), behavioral HR questions, and a day-by-day study plan."
        )

        from guards import generate_content_with_fallback

        response = generate_content_with_fallback(
            client=client,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=InterviewPrepResult,
                temperature=0.3,
            )
        )
        
        return InterviewPrepResult.model_validate_json(response.text)
        
    except Exception as e:
        import logging
        logging.getLogger("interview_coach").error(f"Interview Coach failed: {e}")
        # Graceful fallback in case of rate limits or other API errors
        return InterviewPrepResult(
            technical_questions=[
                TechnicalQuestion(
                    question="Explain the difference between SQL and NoSQL databases, and when you would choose one over the other.",
                    topic="Databases",
                    tips="Discuss ACID properties, scalability, schema flexibility, and use cases."
                ),
                TechnicalQuestion(
                    question="What is the difference between process and thread? How do they communicate?",
                    topic="Operating Systems",
                    tips="Mention memory space sharing, IPC mechanisms, overhead, and context switching."
                ),
                TechnicalQuestion(
                    question="Explain the concept of Object-Oriented Programming (OOP) and its core pillars.",
                    topic="Programming Concepts",
                    tips="Define Encapsulation, Inheritance, Polymorphism, and Abstraction with real-world examples."
                )
            ],
            hr_questions=[
                HRQuestion(
                    question="Tell me about a time you faced a technical challenge in a project and how you resolved it.",
                    rationale="Evaluates problem-solving capability, technical resilience, and critical thinking.",
                    strategy="Use the STAR method (Situation, Task, Action, Result) to structure your answer."
                ),
                HRQuestion(
                    question="Why do you want to join our company?",
                    rationale="Evaluates your research about the company, interest level, and alignment with values.",
                    strategy="Mention specific company values, recent achievements, or projects that interest you and align with your career goals."
                )
            ],
            study_plan=[
                StudyDay(
                    day="Day 1",
                    focus="Data Structures & Algorithms",
                    tasks=["Review Arrays, Strings, Linked Lists", "Solve 2-3 basic problems on LeetCode/GeeksforGeeks"]
                ),
                StudyDay(
                    day="Day 2",
                    focus="Core CS Subjects & System Design",
                    tasks=["Revise Database Management Systems, SQL Queries", "Learn basic System Design concepts (Caching, Load Balancing)"]
                ),
                StudyDay(
                    day="Day 3",
                    focus="Behavioral & HR Prep",
                    tasks=["Prepare STAR stories for top projects", "Practice mock interviews with friends or in front of a mirror"]
                )
            ]
        )
