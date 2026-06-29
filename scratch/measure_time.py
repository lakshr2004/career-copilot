import os
import sys
import time
import asyncio
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from resume_analyzer import analyze_resume_async
from job_matcher import match_job
from interview_coach import generate_prep_plan

load_dotenv()

async def main():
    # Read resume text
    resume_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resume_test.txt")
    with open(resume_path, "r", encoding="utf-8") as f:
        resume_text = f.read()

    print("--- Starting Performance Measurements ---")
    
    # 1. Resume Analyzer
    print("Measuring Resume Analyzer...")
    start = time.time()
    try:
        analysis = await analyze_resume_async(resume_text, github_text="")
        elapsed = time.time() - start
        print(f"Resume Analyzer took: {elapsed:.2f} seconds")
        print(f"ATS Score: {analysis.ats_score}")
    except Exception as e:
        print(f"Resume Analyzer failed: {e}")

    # 2. Job Matcher
    print("\nMeasuring Job Matcher...")
    jd = "Software Engineer job description: Java, Spring Boot, MySQL, Cloud, System Design, REST APIs, Git, Kubernetes, AWS."
    start = time.time()
    try:
        match_res = match_job(resume_text, jd)
        elapsed = time.time() - start
        print(f"Job Matcher took: {elapsed:.2f} seconds")
        print(f"Match Percentage: {match_res.match_percentage}%")
    except Exception as e:
        print(f"Job Matcher failed: {e}")

    # 3. Interview Coach
    print("\nMeasuring Interview Coach...")
    start = time.time()
    try:
        coach_res = generate_prep_plan(resume_text, "Software Engineer")
        elapsed = time.time() - start
        print(f"Interview Coach took: {elapsed:.2f} seconds")
        print(f"Technical Questions Count: {len(coach_res.technical_questions)}")
    except Exception as e:
        print(f"Interview Coach failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
