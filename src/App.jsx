import React, { useState, useEffect } from 'react';
import { 
  Shield, 
  FileText, 
  Briefcase, 
  Compass, 
  Terminal, 
  CheckCircle, 
  Loader2, 
  AlertTriangle, 
  Award, 
  ArrowRight, 
  ChevronDown, 
  ChevronUp, 
  BookOpen, 
  UserCheck, 
  RefreshCw,
  HelpCircle
} from 'lucide-react';

// Custom inline SVG for GitHub logo (since Lucide does not include brand logos)
const Github = ({ className }) => (
  <svg 
    viewBox="0 0 24 24" 
    stroke="currentColor" 
    strokeWidth="2" 
    fill="none" 
    strokeLinecap="round" 
    strokeLinejoin="round" 
    className={className}
  >
    <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22" />
  </svg>
);

export default function App() {
  // Form Inputs
  const [resumeText, setResumeText] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [targetRole, setTargetRole] = useState('Software Engineer');
  const [githubUsername, setGithubUsername] = useState('');
  
  // Pipeline State
  // 'idle' | 'processing_phase1' | 'pending_hitl' | 'processing_phase2' | 'completed' | 'blocked'
  const [pipelineState, setPipelineState] = useState('idle');
  const [workflowStep, setWorkflowStep] = useState(0); 
  const [sessionId, setSessionId] = useState('');
  
  // Data State
  const [resumeAnalysis, setResumeAnalysis] = useState(null);
  const [githubSummary, setGithubSummary] = useState('');
  const [jobMatch, setJobMatch] = useState(null);
  const [interviewPrep, setInterviewPrep] = useState(null);
  const [auditLogs, setAuditLogs] = useState([]);
  const [errorMessage, setErrorMessage] = useState('');
  
  // UI Tabs & Toggles
  const [activeTab, setActiveTab] = useState('dossier'); // 'dossier' | 'resume' | 'matcher' | 'prep'
  const [prepSubTab, setPrepSubTab] = useState('study'); // 'study' | 'technical' | 'hr'
  const [isAuditOpen, setIsAuditOpen] = useState(false);
  const [isSidebarExpanded, setIsSidebarExpanded] = useState(true);
  const [loadingText, setLoadingText] = useState('');
  const [isFileUploading, setIsFileUploading] = useState(false);

  // Added counters states
  const [displayAts, setDisplayAts] = useState(0);
  const [displayMatch, setDisplayMatch] = useState(0);

  const fetchAuditLogs = async () => {
    try {
      const res = await fetch('/api/audit-logs');
      if (res.ok) {
        const data = await res.json();
        setAuditLogs(data);
      }
    } catch (err) {
      console.error('Failed to fetch audit logs:', err);
    }
  };

  // Poll audit logs occasionally
  useEffect(() => {
    fetchAuditLogs();
    const interval = setInterval(fetchAuditLogs, 5000);
    return () => clearInterval(interval);
  }, []);

  // Added interpolation useEffects
  useEffect(() => {
    if (pipelineState === 'completed' && resumeAnalysis?.ats_score) {
      let n = 0;
      const end = resumeAnalysis.ats_score;
      const t = setInterval(() => { n = Math.min(n + 2, end); setDisplayAts(n); if (n >= end) clearInterval(t); }, 18);
      return () => clearInterval(t);
    }
  }, [pipelineState, resumeAnalysis]);

  useEffect(() => {
    if (pipelineState === 'completed' && jobMatch?.match_percentage) {
      let n = 0;
      const end = jobMatch.match_percentage;
      const t = setInterval(() => { n = Math.min(n + 2, end); setDisplayMatch(n); if (n >= end) clearInterval(t); }, 18);
      return () => clearInterval(t);
    }
  }, [pipelineState, jobMatch]);

  const loadSampleData = () => {
    setResumeText(
      "LAKSH RAJ\n" +
      "Full Stack & Machine Learning Engineer\n" +
      "Asansol, West Bengal | 9038138105 | aec.it.lakshraj@gmail.com | LinkedIn\n\n" +
      "PROFESSIONAL SUMMARY\n" +
      "Information Technology undergraduate with a strong foundation in MERN stack development and Machine Learning. " +
      "Proficient in React.js, Node.js, Express, MongoDB, and Python (PyTorch, TensorFlow, Scikit-Learn), with hands-on " +
      "experience building full-stack applications integrated with AI models. Capable of deploying deep learning " +
      "architectures and connecting them to high-performance web interfaces. Focused on clean, maintainable code and scalable systems.\n\n" +
      "EDUCATION\n" +
      "Bachelor of Technology – Information Technology (Pursuing) | Asansol Engineering College, West Bengal\n\n" +
      "PROJECTS\n" +
      "SmartHealth: MERN & AI Diagnostic Platform\n" +
      "An end-to-end healthcare web application allowing patients to upload chest X-rays and receive instant disease classification.\n" +
      "• Built a React.js frontend with Tailwind CSS and a Node.js/Express.js backend utilizing MongoDB for user records\n" +
      "• Developed a FastAPI microservice hosting a PyTorch ResNet-50 image classification model, achieving 94% accuracy\n" +
      "• Integrated JWT authentication and role-based access control, securing API endpoints and user sessions\n\n" +
      "Predictify: Sales Forecasting Dashboard\n" +
      "Full-stack data analysis and forecasting application for e-commerce vendors.\n" +
      "• Implemented an interactive dashboard in React with Recharts for visualizing predictions and historic sales\n" +
      "• Trained and optimized an LSTM neural network in TensorFlow to forecast monthly demand with an RMSE of 12.3\n" +
      "• Built RESTful API endpoints in Express to query forecasted data from PostgreSQL, ensuring less than 150ms response latency\n\n" +
      "TECHNICAL SKILLS\n" +
      "Frontend: React.js, HTML5, CSS3, JavaScript (ES6+), Tailwind CSS, Recharts\n" +
      "Backend: Node.js, Express.js, FastAPI\n" +
      "Databases: PostgreSQL, MongoDB, Redis\n" +
      "Machine Learning: PyTorch, TensorFlow, Scikit-Learn, Pandas, NumPy, Keras\n" +
      "Languages: Python, Java, JavaScript, SQL\n" +
      "Tools: Git, GitHub, Docker, Vite, Visual Studio Code"
    );
    setJobDescription(
      "We are looking for a Software Engineer with expertise in both MERN stack web development and Machine Learning. " +
      "Must have experience with React.js, Node.js, Express, MongoDB, and Python (PyTorch or TensorFlow). " +
      "You will build full-stack interfaces and integrate deep learning models for predictive analysis."
    );
    setTargetRole("Software Engineer");
    setGithubUsername("lakshr2004");
  };


  const handleStartWorkflow = async (e) => {
    e.preventDefault();
    if (!resumeText.trim()) return;

    setErrorMessage('');
    setPipelineState('processing_phase1');
    setWorkflowStep(1); // Scrubbing
    setLoadingText('Scrubbing PII & validating inputs...');
    setActiveTab('dossier');
    
    // Simulate steps in UI for high fidelity feel
    setTimeout(() => {
      setWorkflowStep(2); // Safety Guard check
      setLoadingText('Running safety checks against prompt injection...');
    }, 1200);

    setTimeout(() => {
      setWorkflowStep(3); // GitHub MCP
      setLoadingText(githubUsername ? `Connecting GitHub MCP to retrieve @${githubUsername}...` : 'Skipping GitHub enrichment (no username)...');
    }, 2400);

    setTimeout(() => {
      setWorkflowStep(4); // Analyzing
      setLoadingText('Invoking ResumeAnalyzerAgent (ADK) for placement evaluation...');
    }, 4000);

    try {
      const response = await fetch('/api/orchestrate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          resume_text: resumeText,
          job_description: jobDescription || null,
          target_role: targetRole || null,
          github_username: githubUsername || null
        })
      });

      const data = await response.json();
      fetchAuditLogs();

      if (!response.ok) {
        setPipelineState('blocked');
        setErrorMessage(data.detail || 'Access blocked due to security validation failure.');
        return;
      }

      setSessionId(data.session_id);
      setResumeAnalysis(data.resume_analysis);
      setGithubSummary(data.github_summary);
      setPipelineState('pending_hitl');
      setWorkflowStep(5); // Pending HITL Approval
    } catch (err) {
      setPipelineState('idle');
      setErrorMessage('Failed to connect to backend server. Make sure FastAPI is running.');
    }
  };

  const handleHitlApproval = async (approved) => {
    setPipelineState('processing_phase2');
    setWorkflowStep(6); // Completing pipeline (Matcher & Coach)
    setLoadingText('Finalizing matching and coaching preparation resources...');
    
    try {
      const response = await fetch('/api/hitl-approve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          approved: approved
        })
      });
      
      const data = await response.json();
      fetchAuditLogs();
      
      if (!response.ok) {
        setPipelineState('idle');
        setErrorMessage(data.detail || 'Failed to complete workflow.');
        return;
      }
      
      if (data.status === 'REJECTED') {
        setPipelineState('idle');
        setResumeAnalysis(null);
        setGithubSummary('');
        setSessionId('');
        setActiveTab('dossier');
        return;
      }
      
      setJobMatch(data.results.job_match);
      setInterviewPrep(data.results.interview_prep);
      setPipelineState('completed');
      setWorkflowStep(7); // Completed
      setActiveTab('resume');
    } catch (err) {
      setPipelineState('pending_hitl');
      setErrorMessage('Failed to submit approval.');
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setIsFileUploading(true);
    setErrorMessage('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/extract-text', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to extract text from file.');
      }

      const data = await response.json();
      if (data.text) {
        setResumeText(data.text);
      } else {
        throw new Error('No text content returned from the file.');
      }
    } catch (err) {
      console.error(err);
      setErrorMessage(err.message || 'Failed to extract text. Make sure the file format is supported.');
    } finally {
      setIsFileUploading(false);
      e.target.value = '';
    }
  };

  const handleReset = () => {
    setResumeText('');
    setJobDescription('');
    setTargetRole('Software Engineer');
    setGithubUsername('');
    setPipelineState('idle');
    setWorkflowStep(0);
    setSessionId('');
    setResumeAnalysis(null);
    setJobMatch(null);
    setInterviewPrep(null);
    setErrorMessage('');
    setActiveTab('dossier');
    setPrepSubTab('study');
  };

  return (
    <div style={{ minHeight: '100vh', background: '#F4F1E8', color: '#0A0A0A', paddingBottom: '80px' }}>
      
      {/* SECTION 1: MASTHEAD HEADER */}
      <header style={{ background: '#0A0A0A', borderBottom: '3px solid #D4CFC4' }}>
        {/* Top nameplate bar */}
        <div style={{ borderBottom: '1px solid #333', padding: '8px 40px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <span style={{ fontFamily: 'Courier New, monospace', fontSize: '10px', letterSpacing: '0.2em', color: '#7A756C', textTransform: 'uppercase' }}>
            Est. 2026 · Vol. I · No. 1
          </span>
          <span style={{ fontFamily: 'Georgia, serif', fontSize: '11px', color: '#F4F1E8', letterSpacing: '0.1em' }}>
            PLACEMENT INTELLIGENCE REPORT
          </span>
          <button
            onClick={() => setIsAuditOpen(!isAuditOpen)}
            style={{ background: 'transparent', border: '1px solid #444', color: '#7A756C', fontFamily: 'Courier New, monospace', fontSize: '10px', letterSpacing: '0.15em', textTransform: 'uppercase', padding: '4px 12px', cursor: 'pointer' }}
          >
            Security Log
          </button>
        </div>

        {/* Main masthead */}
        <div style={{ padding: '20px 40px 16px', textAlign: 'center', borderBottom: '1px solid #222' }}>
          <h1 className="masthead-title">
            CareerCopilot <span style={{ color: '#C8102E' }}>AI</span>
          </h1>
          <p style={{ fontFamily: 'Courier New, monospace', fontSize: '10px', color: '#7A756C', letterSpacing: '0.2em', textTransform: 'uppercase', marginTop: '6px' }}>
            Multi-Agent Campus Placement Suite · Indian Engineering Students
          </p>
        </div>

        {/* Ticker bar */}
        <div style={{ background: '#0A0A0A', height: '30px', overflow: 'hidden', display: 'flex', alignItems: 'center' }}>
          <div className="ticker-track" style={{ fontFamily: 'Courier New, monospace', fontSize: '11px', color: '#F4F1E8' }}>
            {/* First copy */}
            <span>ATS SCORE: {resumeAnalysis?.ats_score ?? '—'}</span>
            <span style={{ color: '#C8102E' }}>◆</span>
            <span>JOB MATCH: {jobMatch?.match_percentage ?? '—'}%</span>
            <span style={{ color: '#C8102E' }}>◆</span>
            <span>GITHUB: {githubUsername ? `@${githubUsername} CONNECTED` : 'STANDBY'}</span>
            <span style={{ color: '#C8102E' }}>◆</span>
            <span>PIPELINE: {pipelineState.toUpperCase().replace(/_/g, ' ')}</span>
            <span style={{ color: '#C8102E' }}>◆</span>
            <span>SECURITY: ACTIVE · PII GUARD ON · PROMPT FIREWALL ON</span>
            <span style={{ color: '#C8102E' }}>◆</span>
            {/* Duplicate for seamless loop */}
            <span>ATS SCORE: {resumeAnalysis?.ats_score ?? '—'}</span>
            <span style={{ color: '#C8102E' }}>◆</span>
            <span>JOB MATCH: {jobMatch?.match_percentage ?? '—'}%</span>
            <span style={{ color: '#C8102E' }}>◆</span>
            <span>GITHUB: {githubUsername ? `@${githubUsername} CONNECTED` : 'STANDBY'}</span>
            <span style={{ color: '#C8102E' }}>◆</span>
            <span>PIPELINE: {pipelineState.toUpperCase().replace(/_/g, ' ')}</span>
            <span style={{ color: '#C8102E' }}>◆</span>
            <span>SECURITY: ACTIVE · PII GUARD ON · PROMPT FIREWALL ON</span>
          </div>
        </div>
      </header>

      {/* SECTION 2: MAIN LAYOUT */}
      <main className={`main-layout ${pipelineState !== 'idle' ? 'full-width-report' : ''}`}>
        
        {/* LEFT COLUMN: DOSSIER PANEL */}
        {pipelineState === 'idle' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0', position: 'relative' }}>
          
          {/* WORKFLOW STEPPER */}
          <div style={{ background: '#FFFFFF', border: '1px solid #D4CFC4', padding: '24px' }}>
            <div style={{ marginBottom: '16px' }}>
              <p className="eyebrow" style={{ marginBottom: '8px' }}>Pipeline Status</p>
              <hr className="rule" />
            </div>
            
            {/* Reset button if not idle */}
            {pipelineState !== 'idle' && (
              <button onClick={handleReset} style={{ background: 'transparent', border: 'none', color: '#0A0A0A', fontFamily: 'Courier New, monospace', fontSize: '10px', letterSpacing: '0.1em', textTransform: 'uppercase', cursor: 'pointer', marginBottom: '12px', padding: 0 }}>
                ↺ Reset Pipeline
              </button>
            )}

            {/* Steps list */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0' }}>
              {[
                { label: 'PII Redactor Scrubbing', step: 1 },
                { label: 'Prompt Injection Defense', step: 2 },
                { label: 'GitHub MCP Fetch', step: 3 },
                { label: 'Resume Analyzer (ADK)', step: 4 },
                { label: 'Profile Verification', step: 5 },
                { label: 'Matcher & Coach', step: 6 },
                { label: 'Package Complete', step: 7 },
              ].map((s) => {
                const done = workflowStep > s.step;
                const active = workflowStep === s.step && pipelineState !== 'blocked';
                const blocked = workflowStep === s.step && pipelineState === 'blocked';
                return (
                  <div key={s.step} style={{
                    display: 'flex', alignItems: 'center', gap: '12px',
                    padding: '10px 0',
                    borderLeft: blocked ? '3px solid #C8102E' : active ? '3px solid #C8102E' : done ? '3px solid #0A0A0A' : '3px solid #D4CFC4',
                    paddingLeft: '12px',
                    borderBottom: '1px solid #F4F1E8',
                    background: active ? '#FBF0F2' : 'transparent',
                    transition: 'all 0.2s',
                  }}>
                    <span style={{ fontFamily: 'Courier New, monospace', fontSize: '11px', minWidth: '16px', color: done ? '#0A0A0A' : active ? '#C8102E' : blocked ? '#C8102E' : '#D4CFC4' }}>
                      {done ? '✓' : active ? '●' : blocked ? '✕' : '○'}
                    </span>
                    <span style={{ fontFamily: 'Courier New, monospace', fontSize: '11px', color: done ? '#0A0A0A' : active ? '#C8102E' : blocked ? '#C8102E' : '#B8B2A6', letterSpacing: '0.02em' }}>
                      {s.label}
                    </span>
                    {active && !blocked && <Loader2 style={{ width: 12, height: 12, color: '#0A0A0A', marginLeft: 'auto', animation: 'spin 1s linear infinite' }} />}
                  </div>
                );
              })}
            </div>
          </div>

          {/* INPUT FORM (below stepper, no gap between) */}
          <div style={{ background: '#FFFFFF', border: '1px solid #D4CFC4', borderTop: 'none', padding: '24px', position: 'relative' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: '16px' }}>
              <p className="eyebrow">Submit Dossier</p>
              {pipelineState === 'idle' && (
                <button onClick={loadSampleData} style={{ background: 'transparent', border: 'none', color: '#0A0A0A', fontFamily: 'Courier New, monospace', fontSize: '10px', letterSpacing: '0.1em', textTransform: 'uppercase', cursor: 'pointer', padding: 0, textDecoration: 'underline' }}>
                  Load Sample
                </button>
              )}
            </div>
            <hr className="rule" style={{ marginBottom: '20px' }} />

            <form onSubmit={handleStartWorkflow} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              {/* Curriculum Vitae label */}
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                  <label style={{ fontFamily: 'Courier New, monospace', fontSize: '10px', letterSpacing: '0.15em', textTransform: 'uppercase', color: '#7A756C' }}>
                    Curriculum Vitae *
                  </label>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    {isFileUploading ? (
                      <span style={{ fontFamily: 'Courier New, monospace', fontSize: '10px', color: '#C8102E', textTransform: 'uppercase', display: 'flex', alignItems: 'center', gap: '4px' }}>
                        <Loader2 style={{ width: 10, height: 10, animation: 'spin 1s linear infinite' }} /> Parsing...
                      </span>
                    ) : (
                      <label className="upload-label" style={{
                        cursor: pipelineState === 'idle' ? 'pointer' : 'default',
                        opacity: pipelineState === 'idle' ? 1 : 0.6
                      }}>
                        Upload Resume
                        <input
                          type="file"
                          accept=".txt,.pdf,.docx,.png,.jpg,.jpeg,.webp"
                          onChange={handleFileUpload}
                          disabled={pipelineState !== 'idle'}
                          style={{ display: 'none' }}
                        />
                      </label>
                    )}
                  </div>
                </div>
                <textarea rows={6} placeholder="Paste full resume text, skills, projects, CGPA..." value={resumeText} onChange={e => setResumeText(e.target.value)} disabled={pipelineState !== 'idle' || isFileUploading} required />
              </div>

              <div>
                <label style={{ display: 'block', fontFamily: 'Courier New, monospace', fontSize: '10px', letterSpacing: '0.15em', textTransform: 'uppercase', color: '#7A756C', marginBottom: '6px' }}>
                  Target Position
                </label>
                <textarea rows={4} placeholder="Paste job description to match..." value={jobDescription} onChange={e => setJobDescription(e.target.value)} disabled={pipelineState !== 'idle'} />
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                <div>
                  <label style={{ display: 'block', fontFamily: 'Courier New, monospace', fontSize: '10px', letterSpacing: '0.15em', textTransform: 'uppercase', color: '#7A756C', marginBottom: '6px' }}>
                    Role
                  </label>
                  <select value={targetRole} onChange={e => setTargetRole(e.target.value)} disabled={pipelineState !== 'idle'}>
                    <option value="Software Engineer">SWE</option>
                    <option value="Data Analyst">Data Analyst</option>
                    <option value="Consultant">Consultant</option>
                    <option value="QA Engineer">QA Engineer</option>
                    <option value="Full Stack Web Developer">Full Stack Web Developer</option>
                    <option value="UI/UX Designer">UI/UX Designer</option>
                  </select>
                </div>
                <div>
                  <label style={{ display: 'block', fontFamily: 'Courier New, monospace', fontSize: '10px', letterSpacing: '0.15em', textTransform: 'uppercase', color: '#7A756C', marginBottom: '6px' }}>
                    GitHub Handle
                  </label>
                  <input type="text" placeholder="octocat" value={githubUsername} onChange={e => setGithubUsername(e.target.value)} disabled={pipelineState !== 'idle'} />
                </div>
              </div>

              {pipelineState === 'idle' && (
                <button type="submit" style={{ width: '100%', background: '#0A0A0A', color: '#F4F1E8', border: 'none', padding: '14px', fontFamily: 'Courier New, monospace', fontSize: '11px', letterSpacing: '0.2em', textTransform: 'uppercase', cursor: 'pointer', transition: 'background 0.15s' }}
                  onMouseEnter={e => e.target.style.background = '#C8102E'}
                  onMouseLeave={e => e.target.style.background = '#0A0A0A'}>
                  Analyse Profile →
                </button>
              )}
            </form>

            {/* Loading overlay */}
            {(pipelineState === 'processing_phase1' || pipelineState === 'processing_phase2') && (
              <div style={{ position: 'absolute', inset: 0, background: 'rgba(244,241,232,0.92)', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '12px', zIndex: 10 }}>
                <Loader2 style={{ width: 28, height: 28, color: '#0A0A0A', animation: 'spin 1s linear infinite' }} />
                <p style={{ fontFamily: 'Courier New, monospace', fontSize: '11px', letterSpacing: '0.1em', textTransform: 'uppercase', color: '#0A0A0A', textAlign: 'center', maxWidth: '240px' }}>{loadingText}</p>
              </div>
            )}

            {/* Error */}
            {errorMessage && (
              <div style={{ marginTop: '16px', borderLeft: '3px solid #A31D1D', paddingLeft: '12px', background: '#FBF0F2', padding: '12px 12px 12px 15px' }}>
                <p style={{ fontFamily: 'Courier New, monospace', fontSize: '11px', color: '#A31D1D', letterSpacing: '0.05em' }}>{errorMessage}</p>
              </div>
            )}
          </div>
        </div>
        )}

        {/* RIGHT COLUMN: INTELLIGENCE REPORT */}
        <div style={{ minWidth: 0 }}>
          
          {/* IDLE STATE */}
          {pipelineState === 'idle' && !isFileUploading && (
            <div style={{ background: '#FFFFFF', border: '1px solid #D4CFC4', padding: '48px' }}>
              <p className="eyebrow" style={{ marginBottom: '12px' }}>Awaiting Submission</p>
              <hr style={{ border: 'none', borderTop: '3px solid #0A0A0A', marginBottom: '24px' }} />
              
              <h2 style={{ fontFamily: 'Georgia, serif', fontSize: '36px', fontWeight: 700, lineHeight: 1.2, color: '#0A0A0A', marginBottom: '8px' }}>
                Your placement dossier<br />starts here.
              </h2>
              <p style={{ fontFamily: 'Georgia, serif', fontSize: '15px', color: '#7A756C', marginBottom: '32px', lineHeight: 1.6 }}>
                Submit your resume to receive a comprehensive placement intelligence report — ATS scoring, role alignment, and interview preparation in one pipeline.
              </p>
              
              <hr className="rule" style={{ marginBottom: '32px' }} />

              {/* LETS GET STARTED SECTION */}
              <div style={{ marginBottom: '32px', background: '#F4F1E8', padding: '24px', border: '1px solid #D4CFC4' }}>
                <p className="eyebrow" style={{ color: '#C8102E', fontWeight: 'bold', marginBottom: '12px' }}>Let's Get Started</p>
                <p style={{ fontSize: '13px', color: '#0A0A0A', lineHeight: 1.6, marginBottom: '16px' }}>
                  Prepare your campus placement package in four easy steps using our secure multi-agent system:
                </p>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                  <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
                    <span style={{ fontFamily: 'Courier New, monospace', fontWeight: 'bold', background: '#0A0A0A', color: '#F4F1E8', width: '20px', height: '20px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '11px', flexShrink: 0 }}>1</span>
                    <p style={{ fontSize: '12px', color: '#3A3530', margin: 0 }}><strong>Upload your CV:</strong> Click <strong>Upload Resume</strong> or paste your raw text in the editor. Our PII Engine will redact sensitive information (Aadhar, email, phone) before API transmission.</p>
                  </div>
                  <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
                    <span style={{ fontFamily: 'Courier New, monospace', fontWeight: 'bold', background: '#0A0A0A', color: '#F4F1E8', width: '20px', height: '20px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '11px', flexShrink: 0 }}>2</span>
                    <p style={{ fontSize: '12px', color: '#3A3530', margin: 0 }}><strong>Specify Job Details:</strong> Provide a job description and target role to run a semantic ATS match.</p>
                  </div>
                  <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
                    <span style={{ fontFamily: 'Courier New, monospace', fontWeight: 'bold', background: '#0A0A0A', color: '#F4F1E8', width: '20px', height: '20px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '11px', flexShrink: 0 }}>3</span>
                    <p style={{ fontSize: '12px', color: '#3A3530', margin: 0 }}><strong>Link GitHub Profile:</strong> Provide your GitHub username to connect our GitHub MCP server and retrieve repository metrics.</p>
                  </div>
                  <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
                    <span style={{ fontFamily: 'Courier New, monospace', fontWeight: 'bold', background: '#0A0A0A', color: '#F4F1E8', width: '20px', height: '20px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '11px', flexShrink: 0 }}>4</span>
                    <p style={{ fontSize: '12px', color: '#3A3530', margin: 0 }}><strong>Analyze:</strong> Click <strong>Analyse Profile →</strong> to fire up the secure multi-agent campus placement pipeline.</p>
                  </div>
                </div>
              </div>

              <hr className="rule" style={{ marginBottom: '32px' }} />

              {/* Three feature columns — newspaper style */}
              <div className="responsive-grid-3" style={{ gap: '0' }}>
                {[
                  { num: '01', title: 'Resume Analysis', body: 'ATS scoring, skill extraction, and actionable improvement suggestions tailored for Indian campus hiring.' },
                  { num: '02', title: 'Job Matching', body: 'Semantic alignment between your background and the target role with gap analysis.' },
                  { num: '03', title: 'Interview Prep', body: 'Custom technical and HR questions with recruiter intent decoded and a day-by-day study timeline.' },
                ].map((f, i) => (
                  <div key={i} className={i > 0 ? "border-split-col" : ""} style={{ borderLeft: i > 0 ? '1px solid #D4CFC4' : 'none', paddingLeft: i > 0 ? '24px' : 0, paddingRight: '24px' }}>
                    <p style={{ fontFamily: 'Georgia, serif', fontSize: '32px', fontWeight: 700, color: '#D4CFC4', marginBottom: '4px' }}>{f.num}</p>
                    <p style={{ fontFamily: 'Georgia, serif', fontSize: '14px', fontWeight: 600, color: '#0A0A0A', marginBottom: '8px' }}>{f.title}</p>
                    <p style={{ fontSize: '12px', color: '#7A756C', lineHeight: 1.6 }}>{f.body}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* FILE PARSING STATE */}
          {isFileUploading && (
            <div style={{ background: '#FFFFFF', border: '1px solid #D4CFC4', padding: '48px', minHeight: '400px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '20px' }}>
              <Loader2 style={{ width: 48, height: 48, color: '#C8102E', animation: 'spin 1s linear infinite' }} />
              <p className="eyebrow" style={{ fontSize: '11px', color: '#0A0A0A', letterSpacing: '0.2em' }}>Document Parsing Active</p>
              <h3 style={{ fontFamily: 'Georgia, serif', fontSize: '24px', fontWeight: 700, textAlign: 'center', color: '#0A0A0A', maxWidth: '400px', lineHeight: 1.3 }}>
                Extracting CV content using Google Gemini AI...
              </h3>
              <p style={{ fontSize: '12px', color: '#7A756C', fontFamily: 'Courier New, monospace', textAlign: 'center', maxWidth: '300px' }}>
                Evaluating resume document structure and converting to clean plain text. Please hold on.
              </p>
            </div>
          )}

          {/* PIPELINE PROCESSING STATE */}
          {(pipelineState === 'processing_phase1' || pipelineState === 'processing_phase2') && (
            <div style={{ background: '#FFFFFF', border: '1px solid #D4CFC4', padding: '48px', display: 'flex', flexDirection: 'column', gap: '32px' }}>
              
              <div style={{ textAlign: 'center' }}>
                <p className="eyebrow" style={{ color: '#C8102E', fontSize: '11px', letterSpacing: '0.2em', marginBottom: '8px' }}>Pipeline Active</p>
                <hr style={{ border: 'none', borderTop: '3px solid #C8102E', width: '80px', margin: '0 auto 24px' }} />
                <h2 style={{ fontFamily: 'Georgia, serif', fontSize: '32px', fontWeight: 700, color: '#0A0A0A', marginBottom: '8px' }}>
                  Processing Placement Dossier
                </h2>
                <p style={{ fontSize: '13px', color: '#7A756C' }}>
                  Coordinating multi-agent checks and security verification...
                </p>
              </div>

              {/* Progress Display */}
              <div style={{ maxWidth: '600px', margin: '0 auto', width: '100%', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {[
                  { label: 'PII Redactor Scrubbing', step: 1 },
                  { label: 'Prompt Injection Defense', step: 2 },
                  { label: 'GitHub MCP Fetch', step: 3 },
                  { label: 'Resume Analyzer (ADK)', step: 4 },
                  { label: 'Profile Verification', step: 5 },
                  { label: 'Matcher & Coach', step: 6 },
                  { label: 'Package Complete', step: 7 },
                ].map((s) => {
                  const done = workflowStep > s.step;
                  const active = workflowStep === s.step;
                  return (
                    <div key={s.step} style={{
                      display: 'flex', alignItems: 'center', gap: '16px',
                      padding: '12px 16px',
                      borderLeft: active ? '4px solid #C8102E' : done ? '4px solid #0A0A0A' : '4px solid #D4CFC4',
                      background: active ? '#FBF0F2' : 'transparent',
                      transition: 'all 0.2s',
                    }}>
                      <span style={{ fontFamily: 'Courier New, monospace', fontSize: '13px', minWidth: '24px', fontWeight: 'bold', color: done ? '#0A0A0A' : active ? '#C8102E' : '#D4CFC4' }}>
                        {done ? '✓' : active ? '●' : '○'}
                      </span>
                      <span style={{ fontFamily: 'Courier New, monospace', fontSize: '12px', color: done ? '#0A0A0A' : active ? '#C8102E' : '#B8B2A6', letterSpacing: '0.02em', flex: 1 }}>
                        {s.label}
                      </span>
                      {active && <Loader2 style={{ width: 14, height: 14, color: '#0A0A0A', animation: 'spin 1s linear infinite' }} />}
                    </div>
                  );
                })}
              </div>

              {/* Spinner & Log Statement */}
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '12px', marginTop: '16px', borderTop: '1px solid #D4CFC4', paddingTop: '24px' }}>
                <Loader2 style={{ width: 24, height: 24, color: '#0A0A0A', animation: 'spin 1s linear infinite' }} />
                <p style={{ fontFamily: 'Courier New, monospace', fontSize: '11px', letterSpacing: '0.1em', textTransform: 'uppercase', color: '#0A0A0A', textAlign: 'center', maxWidth: '400px' }}>
                  {loadingText}
                </p>
              </div>

            </div>
          )}

          {/* BLOCKED STATE */}
          {pipelineState === 'blocked' && (
            <div style={{ background: '#FFFFFF', border: '1px solid #D4CFC4', padding: '48px' }}>
              <p className="eyebrow" style={{ marginBottom: '12px', color: '#A31D1D' }}>Access Blocked</p>
              <hr style={{ border: 'none', borderTop: '3px solid #A31D1D', marginBottom: '24px' }} />
              <h2 style={{ fontFamily: 'Georgia, serif', fontSize: '36px', fontWeight: 700, lineHeight: 1.2, color: '#A31D1D', marginBottom: '8px' }}>
                Security Violation Detected.
              </h2>
              <p style={{ fontFamily: 'Georgia, serif', fontSize: '15px', color: '#7A756C', marginBottom: '32px', lineHeight: 1.6 }}>
                The automated safety checker blocked this workflow because a prompt injection attack or administrative bypass instruction was identified.
              </p>
              <hr className="rule" style={{ marginBottom: '32px' }} />
              <div style={{ borderLeft: '3px solid #A31D1D', paddingLeft: '16px', background: '#FBF0F2', padding: '16px' }}>
                <p style={{ fontFamily: 'Courier New, monospace', fontSize: '12px', color: '#A31D1D' }}>
                  <strong>Security Response:</strong> {errorMessage || "Access blocked due to prompt injection attempt."}
                </p>
              </div>
              <button 
                onClick={handleReset} 
                style={{ 
                  marginTop: '24px', 
                  background: '#0A0A0A', 
                  color: '#F4F1E8', 
                  border: 'none', 
                  padding: '12px 24px', 
                  fontFamily: 'Courier New, monospace', 
                  fontSize: '11px', 
                  letterSpacing: '0.15em', 
                  textTransform: 'uppercase', 
                  cursor: 'pointer' 
                }}
                onMouseEnter={e => e.target.style.background = '#C8102E'}
                onMouseLeave={e => e.target.style.background = '#0A0A0A'}
              >
                ↺ Reset & Edit Dossier
              </button>
            </div>
          )}

          {/* PENDING HITL APPROVAL STATE */}
          {pipelineState === 'pending_hitl' && resumeAnalysis && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0' }}>
              {/* Pull-quote approval box */}
              <div style={{ borderLeft: '4px solid #C8102E', background: '#FBF0F2', padding: '24px 28px', marginBottom: '0', border: '1px solid #D4CFC4', borderLeftColor: '#C8102E' }}>
                <p className="eyebrow" style={{ marginBottom: '8px' }}>Human Review Required</p>
                <h3 style={{ fontFamily: 'Georgia, serif', fontSize: '20px', fontWeight: 700, color: '#0A0A0A', marginBottom: '8px' }}>
                  Does this placement profile look accurate?
                </h3>
                <p style={{ fontSize: '13px', color: '#7A756C', marginBottom: '20px' }}>
                  Review the extracted profile below. Approve to proceed to job matching and interview prep, or reject to resubmit.
                </p>
                <div style={{ display: 'flex', gap: '12px' }}>
                  <button onClick={() => handleHitlApproval(true)} style={{ background: '#0A0A0A', color: '#F4F1E8', border: 'none', padding: '12px 28px', fontFamily: 'Courier New, monospace', fontSize: '11px', letterSpacing: '0.15em', textTransform: 'uppercase', cursor: 'pointer' }}
                    onMouseEnter={e => e.target.style.background = '#C8102E'}
                    onMouseLeave={e => e.target.style.background = '#0A0A0A'}>
                    Approve Edition →
                  </button>
                  <button onClick={() => handleHitlApproval(false)} style={{ background: 'transparent', color: '#0A0A0A', border: '1px solid #0A0A0A', padding: '12px 28px', fontFamily: 'Courier New, monospace', fontSize: '11px', letterSpacing: '0.15em', textTransform: 'uppercase', cursor: 'pointer' }}>
                    Reject Draft
                  </button>
                </div>
              </div>

              {/* Resume analysis summary */}
              <div style={{ background: '#FFFFFF', border: '1px solid #D4CFC4', borderTop: 'none', padding: '32px' }}>
                {/* ATS score headline */}
                <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px', marginBottom: '8px' }}>
                  <span style={{ fontFamily: 'Georgia, serif', fontSize: '72px', fontWeight: 700, color: '#0A0A0A', lineHeight: 1 }}>
                    {resumeAnalysis?.ats_score}
                  </span>
                  <span style={{ fontFamily: 'Georgia, serif', fontSize: '20px', color: '#7A756C' }}>/100</span>
                  <span className="eyebrow" style={{ marginLeft: '8px' }}>ATS Score</span>
                </div>
                <hr className="rule" style={{ marginBottom: '24px' }} />

                {/* Two column skills layout */}
                <div className="responsive-grid-2" style={{ marginBottom: '24px' }}>
                  <div>
                    <p className="eyebrow" style={{ marginBottom: '10px' }}>Verified Skills</p>
                    <div>{resumeAnalysis?.extracted_skills?.map((s, i) => <span key={i} className="tag-filled">{s}</span>)}</div>
                  </div>
                  <div>
                    <p className="eyebrow" style={{ marginBottom: '10px' }}>Missing Skills</p>
                    <div>{resumeAnalysis?.missing_skills?.map((s, i) => <span key={i} className="tag-missing">{s}</span>)}</div>
                  </div>
                </div>

                {/* Suggestions */}
                <p className="eyebrow" style={{ marginBottom: '10px' }}>Improvement Actions</p>
                <hr className="rule" style={{ marginBottom: '12px' }} />
                <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                  {resumeAnalysis?.suggestions?.map((s, i) => (
                    <li key={i} style={{ display: 'flex', gap: '10px', fontSize: '13px', color: '#3A3530', lineHeight: 1.5 }}>
                      <span style={{ color: '#7A756C', fontFamily: 'Courier New, monospace', flexShrink: 0 }}>→</span>
                      <span>{s}</span>
                    </li>
                  ))}
                </ul>

                {/* GitHub summary */}
                {githubSummary && (
                  <div style={{ marginTop: '24px', borderTop: '1px solid #D4CFC4', paddingTop: '20px' }}>
                    <p className="eyebrow" style={{ marginBottom: '8px' }}>GitHub Intelligence</p>
                    <pre style={{ fontFamily: 'Courier New, monospace', fontSize: '11px', color: '#7A756C', whiteSpace: 'pre-wrap', lineHeight: 1.6, maxHeight: '120px', overflowY: 'auto' }}>{githubSummary}</pre>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* COMPLETED STATE */}
          {pipelineState === 'completed' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0' }}>
              {/* Edition header */}
              <div style={{ background: '#0A0A0A', padding: '20px 32px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div>
                  <p style={{ fontFamily: 'Courier New, monospace', fontSize: '10px', letterSpacing: '0.15em', color: '#7A756C', textTransform: 'uppercase', marginBottom: '4px' }}>Placement Package · {targetRole}</p>
                  <p style={{ fontFamily: 'Georgia, serif', fontSize: '18px', color: '#F4F1E8', fontWeight: 700 }}>Analysis Complete</p>
                </div>
                <button
                  onClick={handleReset}
                  style={{
                    background: 'transparent',
                    border: '1px solid #C8102E',
                    color: '#C8102E',
                    fontFamily: 'Courier New, monospace',
                    fontSize: '10px',
                    letterSpacing: '0.15em',
                    textTransform: 'uppercase',
                    padding: '8px 16px',
                    cursor: 'pointer',
                    transition: 'all 0.15s ease'
                  }}
                  onMouseEnter={e => {
                    e.target.style.background = '#C8102E';
                    e.target.style.color = '#F4F1E8';
                  }}
                  onMouseLeave={e => {
                    e.target.style.background = 'transparent';
                    e.target.style.color = '#C8102E';
                  }}
                >
                  Clear & Reset
                </button>
                <div style={{ display: 'flex', gap: '24px', textAlign: 'right', alignItems: 'center' }}>
                  <div>
                    <p style={{ fontFamily: 'Georgia, serif', fontSize: '36px', fontWeight: 700, color: '#F4F1E8', lineHeight: 1 }}>{displayAts}</p>
                    <p style={{ fontFamily: 'Courier New, monospace', fontSize: '10px', color: '#7A756C', letterSpacing: '0.1em', textTransform: 'uppercase' }}>ATS Score</p>
                  </div>
                  {jobMatch && (
                    <div>
                      <p style={{ fontFamily: 'Georgia, serif', fontSize: '36px', fontWeight: 700, color: '#C8102E', lineHeight: 1 }}>{displayMatch}%</p>
                      <p style={{ fontFamily: 'Courier New, monospace', fontSize: '10px', color: '#7A756C', letterSpacing: '0.1em', textTransform: 'uppercase' }}>Job Match</p>
                    </div>
                  )}
                </div>
              </div>

              {/* Tab nav */}
              <div style={{ background: '#FFFFFF', borderBottom: '1px solid #D4CFC4', borderLeft: '1px solid #D4CFC4', borderRight: '1px solid #D4CFC4', display: 'flex' }}>
                {[
                  { key: 'resume', label: 'Resume Analysis' },
                  ...(jobMatch ? [{ key: 'matcher', label: 'Job Alignment' }] : []),
                  ...(interviewPrep ? [{ key: 'prep', label: 'Prep Coach' }] : []),
                ].map((tab) => (
                  <button key={tab.key} onClick={() => setActiveTab(tab.key)} style={{
                    background: 'transparent', border: 'none',
                    borderBottom: activeTab === tab.key ? '2px solid #0A0A0A' : '2px solid transparent',
                    padding: '14px 24px',
                    fontFamily: 'Courier New, monospace', fontSize: '10px', letterSpacing: '0.15em', textTransform: 'uppercase',
                    color: activeTab === tab.key ? '#0A0A0A' : '#7A756C',
                    cursor: 'pointer', transition: 'all 0.15s',
                    fontWeight: activeTab === tab.key ? 700 : 400,
                  }}>
                    {tab.label}
                  </button>
                ))}
              </div>

              {/* TAB CONTENT */}
              <div style={{ background: '#FFFFFF', border: '1px solid #D4CFC4', borderTop: 'none', padding: '32px' }} className="fade-in">
                
                {/* RESUME TAB */}
                {activeTab === 'resume' && resumeAnalysis && (
                  <div>
                    <div className="responsive-grid-2" style={{ gap: '48px', marginBottom: '32px' }}>
                      <div>
                        <p className="eyebrow" style={{ marginBottom: '8px' }}>ATS Readiness Score</p>
                        <div style={{ display: 'flex', alignItems: 'baseline', gap: '6px', marginBottom: '16px' }}>
                          <span style={{ fontFamily: 'Georgia, serif', fontSize: '80px', fontWeight: 700, color: '#0A0A0A', lineHeight: 1 }} className="count-up">{displayAts}</span>
                          <span style={{ fontFamily: 'Georgia, serif', fontSize: '24px', color: '#7A756C' }}>/100</span>
                        </div>
                        <hr className="rule" style={{ marginBottom: '16px' }} />
                        <p className="eyebrow" style={{ marginBottom: '10px' }}>Verified Skills ({resumeAnalysis.extracted_skills?.length})</p>
                        <div>{resumeAnalysis.extracted_skills?.map((s, i) => <span key={i} className="tag-filled">{s}</span>)}</div>
                      </div>
                      <div>
                        <p className="eyebrow" style={{ marginBottom: '10px' }}>Missing Core Skills</p>
                        <div style={{ marginBottom: '24px' }}>{resumeAnalysis.missing_skills?.map((s, i) => <span key={i} className="tag-missing">{s}</span>)}</div>
                        <p className="eyebrow" style={{ marginBottom: '10px' }}>Action Items</p>
                        <hr className="rule" style={{ marginBottom: '12px' }} />
                        <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                          {resumeAnalysis.suggestions?.map((s, i) => (
                            <li key={i} style={{ display: 'flex', gap: '10px', fontSize: '13px', color: '#3A3530', lineHeight: 1.5 }}>
                              <span style={{ color: '#7A756C', fontFamily: 'Courier New, monospace', flexShrink: 0 }}>→</span><span>{s}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                )}

                {/* JOB ALIGNMENT TAB */}
                {activeTab === 'matcher' && jobMatch && (
                  <div>
                    <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px', marginBottom: '8px' }}>
                      <span style={{ fontFamily: 'Georgia, serif', fontSize: '80px', fontWeight: 700, color: '#0A0A0A', lineHeight: 1 }} className="count-up">{displayMatch}%</span>
                      <span className="eyebrow">Job Match</span>
                    </div>
                    <hr className="rule" style={{ marginBottom: '24px' }} />
                    <div className="responsive-grid-2" style={{ marginBottom: '24px' }}>
                      <div>
                        <p className="eyebrow" style={{ marginBottom: '10px' }}>Matched Skills</p>
                        <div>{jobMatch.matched_skills?.map((s, i) => <span key={i} className="tag-matched">{s}</span>)}</div>
                      </div>
                      <div>
                        <p className="eyebrow" style={{ marginBottom: '10px' }}>Critical Gaps</p>
                        <div>{jobMatch.missing_skills?.map((s, i) => <span key={i} className="tag-missing">{s}</span>)}</div>
                      </div>
                    </div>
                    <p className="eyebrow" style={{ marginBottom: '10px' }}>Gap Analysis</p>
                    <hr className="rule" style={{ marginBottom: '12px' }} />
                    <p style={{ fontFamily: 'Georgia, serif', fontSize: '14px', color: '#3A3530', lineHeight: 1.8 }}>{jobMatch.gap_analysis}</p>
                  </div>
                )}

                {/* PREP COACH TAB */}
                {activeTab === 'prep' && interviewPrep && (
                  <div>
                    {/* Sub-tabs Nav */}
                    <div className="scrollable-subtabs" style={{ background: '#F4F1E8', border: '1px solid #D4CFC4', display: 'flex', gap: '4px', padding: '4px', marginBottom: '24px' }}>
                      {[
                        { key: 'study', label: '1. Study Plan' },
                        { key: 'technical', label: '2. Technical Q&A' },
                        { key: 'hr', label: '3. HR Q&A' }
                      ].map((subTab) => (
                        <button
                          key={subTab.key}
                          onClick={() => setPrepSubTab(subTab.key)}
                          style={{
                            background: prepSubTab === subTab.key ? '#0A0A0A' : 'transparent',
                            border: 'none',
                            color: prepSubTab === subTab.key ? '#F4F1E8' : '#0A0A0A',
                            padding: '8px 16px',
                            fontFamily: 'Courier New, monospace',
                            fontSize: '11px',
                            fontWeight: 'bold',
                            letterSpacing: '0.1em',
                            textTransform: 'uppercase',
                            cursor: 'pointer',
                            transition: 'all 0.15s',
                            whiteSpace: 'nowrap'
                          }}
                        >
                          {subTab.label}
                        </button>
                      ))}
                    </div>

                    {/* Sub-tab Content */}
                    <div className="fade-in">
                      {/* 1. STUDY PLAN */}
                      {prepSubTab === 'study' && (
                        <div>
                          <p className="eyebrow" style={{ marginBottom: '12px' }}>Day-by-Day Placement Preparation Plan</p>
                          <hr className="rule" style={{ marginBottom: '24px' }} />
                          <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '20px' }}>
                            {interviewPrep.study_plan?.map((day, i) => (
                              <div key={i} style={{ borderLeft: '4px solid #C8102E', paddingLeft: '20px', background: '#FBF0F2', padding: '20px', border: '1px solid #D4CFC4', borderLeftColor: '#C8102E' }}>
                                <p style={{ fontFamily: 'Georgia, serif', fontSize: '28px', fontWeight: 700, color: '#C8102E', lineHeight: 1, marginBottom: '6px' }}>Day {String(i+1).padStart(2,'0')}</p>
                                <p style={{ fontFamily: 'Georgia, serif', fontSize: '15px', fontWeight: 600, color: '#0A0A0A', marginBottom: '12px' }}>{day.focus}</p>
                                <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '8px', padding: 0 }}>
                                  {day.tasks?.map((t, j) => (
                                    <li key={j} style={{ fontSize: '13px', color: '#3A3530', display: 'flex', gap: '8px', lineHeight: 1.5 }}>
                                      <span style={{ color: '#C8102E', fontFamily: 'Courier New, monospace' }}>■</span>
                                      <span>{t}</span>
                                    </li>
                                  ))}
                                </ul>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* 2. TECHNICAL QUESTIONS */}
                      {prepSubTab === 'technical' && (
                        <div>
                          <p className="eyebrow" style={{ marginBottom: '12px' }}>Expected Technical Interview Topics & Questions</p>
                          <hr className="rule" style={{ marginBottom: '24px' }} />
                          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                            {interviewPrep.technical_questions?.map((q, i) => (
                              <div key={i} style={{ borderLeft: '4px solid #0A0A0A', paddingLeft: '20px', background: '#FFFFFF', padding: '20px', border: '1px solid #D4CFC4', borderLeftColor: '#0A0A0A' }}>
                                <span className="tag-filled" style={{ marginBottom: '10px' }}>{q.topic}</span>
                                <p style={{ fontSize: '15px', fontWeight: 600, color: '#0A0A0A', marginBottom: '8px', fontFamily: 'Georgia, serif' }}>Q: {q.question}</p>
                                <p style={{ fontSize: '13px', color: '#7A756C', borderTop: '1px solid #F4F1E8', paddingTop: '10px', marginTop: '10px' }}><strong>Tip:</strong> {q.tips}</p>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* 3. HR QUESTIONS */}
                      {prepSubTab === 'hr' && (
                        <div>
                          <p className="eyebrow" style={{ marginBottom: '12px' }}>Recruiter Behavioral & HR Q&A</p>
                          <hr className="rule" style={{ marginBottom: '24px' }} />
                          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                            {interviewPrep.hr_questions?.map((q, i) => (
                              <div key={i} style={{ borderLeft: '4px solid #7A756C', paddingLeft: '20px', background: '#FFFFFF', padding: '20px', border: '1px solid #D4CFC4', borderLeftColor: '#7A756C' }}>
                                <p style={{ fontSize: '15px', fontWeight: 600, color: '#0A0A0A', marginBottom: '12px', fontFamily: 'Georgia, serif' }}>Q: {q.question}</p>
                                <p style={{ fontSize: '13px', color: '#3A3530', marginBottom: '8px', lineHeight: 1.5 }}><strong>Recruiter Intent:</strong> {q.rationale}</p>
                                <p style={{ fontSize: '13px', color: '#7A756C', lineHeight: 1.5, borderTop: '1px solid #F4F1E8', paddingTop: '10px', marginTop: '10px' }}><strong>Response Strategy:</strong> {q.strategy}</p>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

        </div>
      </main>

      {/* AUDIT DRAWER */}
      <div style={{
        position: 'fixed', bottom: 0, left: 0, right: 0, zIndex: 50,
        background: '#0A0A0A',
        borderTop: '1px solid #C8102E',
        height: isAuditOpen ? '320px' : '36px',
        transition: 'height 0.25s ease',
        overflow: 'hidden',
      }}>
        {/* Toggle bar */}
        <div onClick={() => setIsAuditOpen(!isAuditOpen)} style={{ height: '36px', padding: '0 32px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', cursor: 'pointer', borderBottom: isAuditOpen ? '1px solid #222' : 'none' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <Shield style={{ width: 12, height: 12, color: '#C8102E' }} />
            <span style={{ fontFamily: 'Courier New, monospace', fontSize: '10px', letterSpacing: '0.2em', textTransform: 'uppercase', color: '#7A756C' }}>Security Log</span>
            <span style={{ fontFamily: 'Courier New, monospace', fontSize: '10px', color: '#444', marginLeft: '8px' }}>{auditLogs.length} events</span>
          </div>
          {isAuditOpen ? <ChevronDown style={{ width: 12, height: 12, color: '#7A756C' }} /> : <ChevronUp style={{ width: 12, height: 12, color: '#7A756C' }} />}
        </div>

        {/* Log content */}
        <div style={{ height: 'calc(100% - 36px)', overflowY: 'auto', padding: '16px 32px' }}>
          {auditLogs.length === 0 ? (
            <p style={{ fontFamily: 'Courier New, monospace', fontSize: '11px', color: '#444', textAlign: 'center', paddingTop: '32px' }}>No events logged. Run the pipeline to generate security audit entries.</p>
          ) : (
            auditLogs.map((log, idx) => {
              const isSuccess = ['SUCCESS','CLEAN','PASSED','APPROVED'].includes(log.status);
              const isWarn = ['REDACTED','BLOCKED','WARNING'].includes(log.status);
              const isError = ['ERROR','EXCEPTION'].includes(log.status);
              const statusColor = isSuccess ? '#4ade80' : isWarn ? '#fbbf24' : isError ? '#f87171' : '#7A756C';
              const time = new Date(log.timestamp).toLocaleTimeString();
              return (
                <div key={idx} style={{ display: 'flex', gap: '12px', padding: '4px 0', fontFamily: 'Courier New, monospace', fontSize: '11px', borderBottom: '1px solid #111' }}>
                  <span style={{ color: '#444', flexShrink: 0 }}>[{time}]</span>
                  <span style={{ color: '#7A756C', textTransform: 'uppercase', letterSpacing: '0.05em', flexShrink: 0 }}>{log.action}</span>
                  <span style={{ color: statusColor, flexShrink: 0 }}>[{log.status}]</span>
                  <span style={{ color: '#555', flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{JSON.stringify(log.details)}</span>
                </div>
              );
            })
          )}
        </div>
      </div>

    </div>
  );
}
