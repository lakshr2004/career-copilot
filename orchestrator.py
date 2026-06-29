import uuid
import logging
from typing import Dict, Any, Optional
from guards import scrub_pii, detect_prompt_injection, log_audit
from github_mcp import get_github_summary
from resume_analyzer import analyze_resume_async, ResumeAnalysisResult
from job_matcher import match_job, JobMatchResult
from interview_coach import generate_prep_plan, InterviewPrepResult

logger = logging.getLogger("orchestrator")

# In-memory storage for active sessions
sessions: Dict[str, Dict[str, Any]] = {}

class OrchestratorError(Exception):
    def __init__(self, message: str, code: str = "ERROR"):
        super().__init__(message)
        self.code = code

async def start_placement_workflow(
    resume_text: str,
    job_description: Optional[str] = None,
    target_role: Optional[str] = None,
    github_username: Optional[str] = None
) -> Dict[str, Any]:
    """
    Phase 1: Validates inputs, scrubs PII, checks for prompt injection,
    enriches profile with GitHub repos (MCP/HTTP), runs the Resume Analyzer Agent,
    and returns intermediate results for human verification.
    """
    session_id = str(uuid.uuid4())
    log_audit("workflow_start", "INITIATED", {"session_id": session_id, "github_username": github_username})
    
    # 1. Prompt Injection Detection
    raw_inputs = [resume_text]
    if job_description:
        raw_inputs.append(job_description)
    if target_role:
        raw_inputs.append(target_role)
    if github_username:
        raw_inputs.append(github_username)
        
    combined_input = "\n".join(raw_inputs)
    if detect_prompt_injection(combined_input):
        log_audit("workflow_start", "BLOCKED", {"session_id": session_id, "reason": "Prompt injection detected"})
        sessions[session_id] = {
            "status": "BLOCKED",
            "error": "Security violation: prompt injection attempt detected."
        }
        raise OrchestratorError("Security violation: prompt injection attempt detected.", "SECURITY_BLOCKED")
        
    # 2. PII Scrubbing
    scrubbed_resume = scrub_pii(resume_text)
    scrubbed_jd = scrub_pii(job_description) if job_description else None
    
    # Save processed inputs
    sessions[session_id] = {
        "session_id": session_id,
        "status": "PENDING_HITL",
        "inputs": {
            "resume_text": scrubbed_resume,
            "job_description": scrubbed_jd,
            "target_role": target_role,
            "github_username": github_username
        },
        "intermediate_results": {},
        "final_results": {}
    }
    
    # 3. Fetch GitHub repositories dynamically
    github_summary = ""
    if github_username:
        try:
            github_summary = await get_github_summary(github_username)
        except Exception as e:
            logger.warning(f"Error fetching GitHub profile: {e}")
            github_summary = f"GitHub Profile for '{github_username}': Failed to fetch data."
            log_audit("github_fetch", "FAILED", {"session_id": session_id, "error": str(e)})

    # 4. Execute Resume Analyzer Agent (google-adk)
    logger.info(f"Running ResumeAnalyzerAgent for session: {session_id}...")
    try:
        resume_analysis = await analyze_resume_async(scrubbed_resume, github_summary)
        
        # Save results to session
        sessions[session_id]["intermediate_results"] = {
            "resume_analysis": resume_analysis.model_dump(),
            "github_summary": github_summary
        }
        
        log_audit("resume_analysis", "SUCCESS", {"session_id": session_id, "ats_score": resume_analysis.ats_score})
        
        return {
            "session_id": session_id,
            "status": "PENDING_HITL",
            "resume_analysis": resume_analysis.model_dump(),
            "github_summary": github_summary
        }
        
    except Exception as e:
        log_audit("resume_analysis", "FAILED", {"session_id": session_id, "error": str(e)})
        sessions[session_id]["status"] = "FAILED"
        raise OrchestratorError(f"Failed to analyze resume: {e}", "ANALYSIS_FAILED")

async def approve_and_complete_workflow(session_id: str, approved: bool) -> Dict[str, Any]:
    """
    Phase 2: Processes the HITL review step. If approved, executes the Job Matcher Agent
    and Interview Coach Agent to finalize the full placement prep output.
    """
    if session_id not in sessions:
        raise OrchestratorError("Session not found.", "NOT_FOUND")
        
    session = sessions[session_id]
    
    if session["status"] != "PENDING_HITL":
        raise OrchestratorError(f"Invalid workflow state: {session['status']}", "INVALID_STATE")
        
    if not approved:
        session["status"] = "REJECTED"
        log_audit("workflow_approval", "REJECTED", {"session_id": session_id})
        return {
            "session_id": session_id,
            "status": "REJECTED",
            "message": "Workflow profile rejected by user."
        }
        
    log_audit("workflow_approval", "APPROVED", {"session_id": session_id})
    session["status"] = "COMPLETING"
    
    inputs = session["inputs"]
    resume_text = inputs["resume_text"]
    job_description = inputs["job_description"]
    target_role = inputs["target_role"]
    
    # Run Job Matcher (if JD is provided)
    job_match_data = None
    if job_description:
        logger.info(f"Running Job Matcher for session: {session_id}...")
        try:
            match_res = match_job(resume_text, job_description)
            job_match_data = match_res.model_dump()
            log_audit("job_match", "SUCCESS", {"session_id": session_id, "percentage": match_res.match_percentage})
        except Exception as e:
            logger.error(f"Job Matcher failed: {e}")
            log_audit("job_match", "FAILED", {"session_id": session_id, "error": str(e)})
            job_match_data = {"error": "Failed to run job matcher."}
            
    # Run Interview Coach (if target role is specified)
    interview_prep_data = None
    if target_role:
        logger.info(f"Running Interview Coach for session: {session_id}...")
        try:
            coach_res = generate_prep_plan(resume_text, target_role)
            interview_prep_data = coach_res.model_dump()
            log_audit("interview_prep", "SUCCESS", {"session_id": session_id})
        except Exception as e:
            logger.error(f"Interview Coach failed: {e}")
            log_audit("interview_prep", "FAILED", {"session_id": session_id, "error": str(e)})
            interview_prep_data = {"error": "Failed to run interview coach."}
            
    # Assemble final package
    final_output = {
        "resume_analysis": session["intermediate_results"]["resume_analysis"],
        "github_summary": session["intermediate_results"]["github_summary"],
        "job_match": job_match_data,
        "interview_prep": interview_prep_data
    }
    
    session["final_results"] = final_output
    session["status"] = "COMPLETED"
    
    log_audit("workflow_complete", "SUCCESS", {"session_id": session_id})
    
    return {
        "session_id": session_id,
        "status": "COMPLETED",
        "results": final_output
    }
