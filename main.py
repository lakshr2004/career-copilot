import os
import logging
from typing import Optional, List
from fastapi import FastAPI, HTTPException, status, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn
from dotenv import load_dotenv

# Import our orchestration components
from orchestrator import (
    start_placement_workflow,
    approve_and_complete_workflow,
    OrchestratorError,
    sessions
)
from resume_analyzer import analyze_resume_async
from job_matcher import match_job
from interview_coach import generate_prep_plan
from guards import log_audit, AUDIT_LOG_PATH

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

app = FastAPI(
    title="CareerCopilot AI Backend",
    description="Multi-agent Indian Campus Placement Preparation System",
    version="1.0.0"
)

# Configure CORS so React (running on Vite dev port 5173 or others) can connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In development, allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic schemas for request bodies
class OrchestrateRequest(BaseModel):
    resume_text: str = Field(..., min_length=10, description="Raw text content of the candidate's resume")
    job_description: Optional[str] = Field(None, description="Job description text for keyword match")
    target_role: Optional[str] = Field(None, description="Job role student is preparing for")
    github_username: Optional[str] = Field(None, description="Candidate's GitHub username")

class ApproveRequest(BaseModel):
    session_id: str = Field(..., description="Unique workflow session ID")
    approved: bool = Field(..., description="Student approval status")

class AnalyzeResumeRequest(BaseModel):
    resume_text: str
    github_username: Optional[str] = None

class MatchJobRequest(BaseModel):
    resume_text: str
    job_description: str

class InterviewPrepRequest(BaseModel):
    resume_text: str
    target_role: str

# API Routes
@app.get("/")
def read_root():
    return {"message": "Welcome to CareerCopilot AI API Service", "status": "active"}

@app.post("/api/orchestrate")
async def api_orchestrate(req: OrchestrateRequest):
    try:
        result = await start_placement_workflow(
            resume_text=req.resume_text,
            job_description=req.job_description,
            target_role=req.target_role,
            github_username=req.github_username
        )
        return result
    except OrchestratorError as e:
        if e.code == "SECURITY_BLOCKED":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        logger.error(f"Error in orchestrate endpoint: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.post("/api/hitl-approve")
async def api_hitl_approve(req: ApproveRequest):
    try:
        result = await approve_and_complete_workflow(req.session_id, req.approved)
        return result
    except OrchestratorError as e:
        if e.code == "NOT_FOUND":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error in hitl-approve endpoint: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/api/audit-logs")
def api_audit_logs():
    """
    Fetches system security audit logs from security/audit.log.
    Returns the last 50 entries.
    """
    if not os.path.exists(AUDIT_LOG_PATH):
        return []
        
    try:
        logs = []
        with open(AUDIT_LOG_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    import json
                    try:
                        logs.append(json.loads(line.strip()))
                    except Exception:
                        pass
        # Return last 50 logs (newest first)
        return list(reversed(logs[-50:]))
    except Exception as e:
        logger.error(f"Failed to read audit logs: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to read audit logs: {e}")

@app.post("/api/extract-text")
async def api_extract_text(file: UploadFile = File(...)):
    filename = file.filename or ""
    content_type = file.content_type or ""
    file_bytes = await file.read()
    
    # 1. Plain text extraction
    if filename.endswith(".txt") or "text/plain" in content_type:
        try:
            text = file_bytes.decode("utf-8")
            return {"text": text}
        except Exception as e:
            try:
                text = file_bytes.decode("latin1")
                return {"text": text}
            except Exception as e2:
                raise HTTPException(status_code=400, detail=f"Failed to decode text file: {e2}")

    # 2. Binary document extraction via Gemini fallback
    mime_map = {
        ".pdf": "application/pdf",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    }
    
    ext = os.path.splitext(filename.lower())[1]
    mapped_mime = mime_map.get(ext, content_type)
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="GOOGLE_API_KEY is not configured in the backend environment. Cannot extract text from binary files."
        )
        
    try:
        from google import genai
        from google.genai import types
        from guards import generate_content_with_fallback
        
        client = genai.Client(api_key=api_key)
        
        part = types.Part.from_bytes(
            data=file_bytes,
            mime_type=mapped_mime
        )
        
        prompt = (
            "You are a document text extraction assistant. "
            "Please extract and transcribe the exact text content from this resume document. "
            "Maintain the layout structure, section headings, and content exactly as written. "
            "Do not summarize, do not omit details, and do not add any commentary, conversational intro/outro, or markdown formatting blocks (such as ```). "
            "Output only the extracted plain text of the document."
        )
        
        response = generate_content_with_fallback(
            client=client,
            contents=[part, prompt],
            config=types.GenerateContentConfig(
                temperature=0.0
            )
        )
        
        return {"text": response.text.strip()}
    except Exception as e:
        logger.error(f"Error extracting text via Gemini: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to extract text from file: {str(e)}"
        )

# Individual routes for debug/direct access
@app.post("/api/analyze-resume")
async def api_analyze_resume(req: AnalyzeResumeRequest):
    github_summary = ""
    if req.github_username:
        from github_mcp import get_github_summary
        github_summary = await get_github_summary(req.github_username)
    try:
        result = await analyze_resume_async(req.resume_text, github_summary)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/match-job")
def api_match_job(req: MatchJobRequest):
    try:
        result = match_job(req.resume_text, req.job_description)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/interview-prep")
def api_interview_prep(req: InterviewPrepRequest):
    try:
        result = generate_prep_plan(req.resume_text, req.target_role)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    # Run FastAPI server
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
