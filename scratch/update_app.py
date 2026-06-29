import os

app_path = r"c:\Users\Laksh\Desktop\career-copilot\src\App.jsx"

# The new code to append starting from the return statement
new_code_part = """  const navItems = [
    { id: 'dossier', label: 'Dossier Input', icon: Compass, enabled: true },
    { id: 'resume', label: 'Resume Analysis', icon: Award, enabled: resumeAnalysis !== null },
    { id: 'matcher', label: 'Job Alignment', icon: Briefcase, enabled: jobMatch !== null },
    { id: 'prep', label: 'Placement Coach', icon: BookOpen, enabled: interviewPrep !== null }
  ];

  return (
    <div className="min-h-screen flex flex-col relative overflow-hidden font-sans" style={{background:'#F7F5F0', color:'#111111'}}>
      
      {/* Newspaper Masthead */}
      <header className="w-full py-4 px-6 md:px-12 sticky top-0 z-40 bg-[#111111]" style={{borderBottom:'1px solid #333333'}}>
        <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 items-center gap-3 md:gap-0">
          {/* Left */}
          <div className="flex items-center space-x-3 justify-center md:justify-start">
            <button 
              onClick={() => setIsSidebarExpanded(!isSidebarExpanded)}
              className="p-1.5 hover:bg-[#333333] text-[#F7F5F0] transition-colors cursor-pointer rounded-none"
              title="Toggle Sidebar"
            >
              <span className="text-lg leading-none block w-4 text-center">☰</span>
            </button>
            <Compass className="h-5 w-5 text-[#F7F5F0]" />
            <span className="text-[11px] uppercase tracking-[0.2em] font-sans text-[#888888] hidden sm:inline">
              CAREERCOPILOT AI
            </span>
          </div>

          {/* Center */}
          <div className="text-center">
            <h1 className="font-serif text-xl text-[#F7F5F0] font-bold tracking-wide">
              Placement Intelligence
            </h1>
          </div>

          {/* Right */}
          <div className="flex items-center justify-center md:justify-end space-x-4">
            <span className="text-[10px] font-mono text-[#888888] hidden sm:inline">
              {new Date().toLocaleDateString('en-US', { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' }).toUpperCase()} | EST. 2026
            </span>
            <button 
              onClick={() => setIsAuditOpen(!isAuditOpen)}
              className="px-3 py-1.5 border border-[#D9D4C7] bg-transparent text-[#F7F5F0] text-[10px] uppercase tracking-wider font-mono flex items-center gap-1.5 transition-all cursor-pointer rounded-none"
            >
              <Terminal className="h-3.5 w-3.5" />
              Audit Logs
            </button>
          </div>
        </div>
      </header>

      {/* News Ticker Bar */}
      <div style={{background:'#111111', borderBottom:'1px solid #333', overflow:'hidden', height:'28px'}}>
        <div style={{display:'flex', alignItems:'center', height:'100%', animation:'ticker 20s linear infinite', whiteSpace:'nowrap', fontFamily:'monospace', fontSize:'11px', color:'#F7F5F0', gap:'48px', paddingLeft:'100%'}}>
          <span>ATS SCORE: {resumeAnalysis?.ats_score ?? '--'}</span>
          <span style={{color:'#C8102E'}}>◆</span>
          <span>JOB MATCH: {jobMatch?.match_percentage ?? '--'}%</span>
          <span style={{color:'#C8102E'}}>◆</span>
          <span>GITHUB MCP: {githubUsername ? 'CONNECTED' : 'STANDBY'}</span>
          <span style={{color:'#C8102E'}}>◆</span>
          <span>STATUS: {pipelineState.toUpperCase().replace('_',' ')}</span>
          <span style={{color:'#C8102E'}}>◆</span>
          <span>ATS SCORE: {resumeAnalysis?.ats_score ?? '--'}</span>
          <span style={{color:'#C8102E'}}>◆</span>
          <span>JOB MATCH: {jobMatch?.match_percentage ?? '--'}%</span>
        </div>
      </div>

      {/* App Main Layout Structure */}
      <div className="flex-1 flex flex-row min-h-0 relative">
        
        {/* Mobile Sidebar Overlay */}
        {isSidebarExpanded && (
          <div 
            className="fixed inset-0 bg-[#111111]/30 z-20 md:hidden"
            onClick={() => setIsSidebarExpanded(false)}
          />
        )}

        {/* Collapsible Left Vertical Sidebar Navigation (YouTube Style) */}
        <aside 
          className={`shrink-0 transition-all duration-200 bg-[#FFFFFF] border-r border-[#D9D4C7] select-none ${
            isSidebarExpanded ? 'w-[240px]' : 'w-[72px]'
          } ${isSidebarExpanded ? 'fixed md:static inset-y-0 left-0 z-30 block' : 'hidden md:block'}`}
        >
          <div className="flex flex-col py-3 h-full justify-between">
            <div className="space-y-1">
              {navItems.map((item) => {
                const IconComponent = item.icon;
                const isActive = (pipelineState === 'completed' && activeTab === item.id) || (pipelineState !== 'completed' && item.id === 'dossier');
                
                if (isSidebarExpanded) {
                  return (
                    <button
                      key={item.id}
                      disabled={!item.enabled}
                      onClick={() => item.enabled && setActiveTab(item.id)}
                      className={`w-full flex items-center gap-4 px-4 py-3 text-[11px] uppercase tracking-wider font-semibold border-l-[3px] transition-all duration-150 text-left ${
                        isActive 
                          ? 'bg-[#111111] text-[#F7F5F0] border-[#C8102E]' 
                          : 'bg-transparent text-[#111111] border-transparent hover:bg-[#F7F5F0]'
                      } ${!item.enabled ? 'opacity-30 cursor-not-allowed' : 'cursor-pointer'}`}
                    >
                      <IconComponent className="h-4.5 w-4.5 shrink-0" />
                      <span>{item.label}</span>
                    </button>
                  );
                } else {
                  return (
                    <button
                      key={item.id}
                      disabled={!item.enabled}
                      onClick={() => item.enabled && setActiveTab(item.id)}
                      className={`w-full flex flex-col items-center justify-center py-4 border-l-[3px] transition-all duration-150 ${
                        isActive 
                          ? 'bg-[#111111] text-[#F7F5F0] border-[#C8102E]' 
                          : 'bg-transparent text-[#111111] border-transparent hover:bg-[#F7F5F0]'
                      } ${!item.enabled ? 'opacity-30 cursor-not-allowed' : 'cursor-pointer'}`}
                    >
                      <IconComponent className="h-4.5 w-4.5" />
                      <span className="text-[8px] uppercase tracking-tighter mt-1">{item.label.split(' ')[0]}</span>
                    </button>
                  );
                }
              })}
            </div>

            {/* Sidebar Footer Log Toggle Action */}
            <div className="border-t border-[#D9D4C7]/50 pt-2">
              <button
                onClick={() => setIsAuditOpen(!isAuditOpen)}
                className={`w-full flex items-center transition-all duration-150 text-left ${
                  isSidebarExpanded 
                    ? 'px-4 py-3 gap-4 text-[11px] uppercase tracking-wider font-semibold text-[#111111] hover:bg-[#F7F5F0]' 
                    : 'flex-col justify-center py-4 text-[#111111] hover:bg-[#F7F5F0]'
                }`}
              >
                <Shield className="h-4.5 w-4.5 text-[#111111]" />
                {isSidebarExpanded ? (
                  <span>Security Logs</span>
                ) : (
                  <span className="text-[8px] uppercase tracking-tighter mt-1">Logs</span>
                )}
              </button>
            </div>
          </div>
        </aside>

        {/* Main Workspace Area */}
        <main className="flex-1 overflow-y-auto p-6 md:p-10 pb-24 min-w-0">
          <div className="max-w-7xl mx-auto">

            {/* View 1: Dossier Input View */}
            {((pipelineState !== 'completed') || (pipelineState === 'completed' && activeTab === 'dossier')) && (
              <div className="flex flex-col lg:flex-row gap-8">
                
                {/* Left Side: Input Form & Workflow Steps */}
                <div className="w-full lg:w-[420px] flex flex-col gap-6 shrink-0">
                  
                  {/* Stepper Card */}
                  <div style={{background:'#FFFFFF', border:'1px solid #D9D4C7', padding:'1.5rem'}} className="rounded-none">
                    <div className="flex items-center justify-between border-b border-[#D9D4C7] pb-2 mb-4">
                      <h3 className="text-[10px] uppercase tracking-[0.15em] text-[#888888] font-sans font-bold">
                        Workflow Status
                      </h3>
                      {pipelineState !== 'idle' && (
                        <button onClick={handleReset} className="text-[10px] uppercase tracking-wider text-[#C8102E] font-sans font-bold underline hover:text-[#111111] flex items-center gap-1 transition-colors">
                          <RefreshCw className="h-3 w-3" /> Reset
                        </button>
                      )}
                    </div>
                    
                    {/* Steps Timeline */}
                    <div className="space-y-2 font-mono text-[11px]">
                      {[
                        { label: 'PII Redactor Scrubbing', step: 1 },
                        { label: 'Prompt Injection Defense', step: 2 },
                        { label: 'GitHub MCP tech-extract', step: 3 },
                        { label: 'Resume Analyzer Agent (ADK)', step: 4 },
                        { label: 'Student Profile Verification', step: 5 },
                        { label: 'Matcher & Coach generation', step: 6 },
                        { label: 'Completed Package', step: 7 }
                      ].map((s) => {
                        let borderStyle = "border-l-[3px] border-[#D9D4C7] text-[#888888]";
                        let statusIndicator = null;

                        if (workflowStep === s.step) {
                          if (pipelineState === 'blocked') {
                            borderStyle = "border-l-[3px] border-[#C8102E] text-[#C8102E] font-bold";
                            statusIndicator = <AlertTriangle className="h-3.5 w-3.5 text-[#C8102E] shrink-0" />;
                          } else {
                            borderStyle = "border-l-[3px] border-[#C8102E] text-[#C8102E] font-bold";
                            statusIndicator = <Loader2 className="h-3.5 w-3.5 text-[#C8102E] animate-spin shrink-0" />;
                          }
                        } else if (workflowStep > s.step) {
                          borderStyle = "border-l-[3px] border-[#111111] text-[#111111] font-semibold";
                          statusIndicator = <span className="text-[#111111] font-bold">✓</span>;
                        }

                        return (
                          <div 
                            key={s.step} 
                            className={`flex items-center justify-between p-2.5 rounded-none border-b border-t-0 border-r-0 border-l-0 border-[#D9D4C7]/50 ${borderStyle} transition-colors duration-350`}
                          >
                            <span className="truncate mr-2">{s.label}</span>
                            {statusIndicator && (
                              <div className="w-5 h-5 flex items-center justify-center shrink-0">
                                {statusIndicator}
                              </div>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  </div>

                  {/* Input Panel Card */}
                  <div style={{background:'#FFFFFF', border:'1px solid #D9D4C7', padding:'1.5rem'}} className="rounded-none relative">
                    <div className="flex items-center justify-between border-b border-[#D9D4C7] pb-2 mb-4">
                      <h3 className="text-[10px] uppercase tracking-[0.15em] text-[#888888] font-sans font-bold">Placement Details</h3>
                      {pipelineState === 'idle' && (
                        <button 
                          onClick={loadSampleData} 
                          className="text-[11px] text-[#C8102E] uppercase tracking-wider underline font-sans font-semibold cursor-pointer"
                        >
                          Load Sample Student
                        </button>
                      )}
                    </div>

                    <form onSubmit={handleStartWorkflow} className="space-y-4">
                      <div>
                        <label className="text-[10px] uppercase tracking-[0.15em] text-[#888888] font-sans block mb-1.5 flex items-center gap-1.5">
                          <FileText className="h-3.5 w-3.5 text-[#888888]" /> Resume Content (Text)*
                        </label>
                        <textarea
                          className="w-full h-32 p-3 border border-[#D9D4C7] bg-white rounded-none text-[#111] text-sm focus:border-[#111] focus:outline-none resize-none font-sans"
                          placeholder="Paste raw resume text, projects, skills, CGPA..."
                          value={resumeText}
                          onChange={(e) => setResumeText(e.target.value)}
                          disabled={pipelineState !== 'idle'}
                          required
                        />
                      </div>

                      <div>
                        <label className="text-[10px] uppercase tracking-[0.15em] text-[#888888] font-sans block mb-1.5 flex items-center gap-1.5">
                          <Briefcase className="h-3.5 w-3.5 text-[#888888]" /> Job Description (Optional)
                        </label>
                        <textarea
                          className="w-full h-24 p-3 border border-[#D9D4C7] bg-white rounded-none text-[#111] text-sm focus:border-[#111] focus:outline-none resize-none font-sans"
                          placeholder="Paste target job description to match skills..."
                          value={jobDescription}
                          onChange={(e) => setJobDescription(e.target.value)}
                          disabled={pipelineState !== 'idle'}
                        />
                      </div>

                      <div className="grid grid-cols-2 gap-3">
                        <div>
                          <label className="text-[10px] uppercase tracking-[0.15em] text-[#888888] font-sans block mb-1.5">
                            Target Role
                          </label>
                          <select
                            className="w-full p-2.5 border border-[#D9D4C7] bg-white rounded-none text-[#111] text-sm focus:border-[#111] focus:outline-none font-sans"
                            value={targetRole}
                            onChange={(e) => setTargetRole(e.target.value)}
                            disabled={pipelineState !== 'idle'}
                          >
                            <option value="Software Engineer">SWE</option>
                            <option value="Data Analyst">Data Analyst</option>
                            <option value="Consultant">Consultant</option>
                            <option value="QA Engineer">QA Engineer</option>
                          </select>
                        </div>
                        <div>
                          <label className="text-[10px] uppercase tracking-[0.15em] text-[#888888] font-sans block mb-1.5 flex items-center gap-1.5">
                            <Github className="h-3.5 w-3.5 text-[#888888]" /> GitHub User
                          </label>
                          <input
                            type="text"
                            className="w-full p-2 border border-[#D9D4C7] bg-white rounded-none text-[#111] text-sm focus:border-[#111] focus:outline-none font-sans"
                            placeholder="e.g. octocat"
                            value={githubUsername}
                            onChange={(e) => setGithubUsername(e.target.value)}
                            disabled={pipelineState !== 'idle'}
                          />
                        </div>
                      </div>

                      {pipelineState === 'idle' && (
                        <button
                          type="submit"
                          className="w-full py-3 px-4 bg-[#111111] text-[#F7F5F0] rounded-none text-[11px] uppercase tracking-[0.15em] font-semibold hover:bg-[#C8102E] transition-colors flex items-center justify-center space-x-1.5 cursor-pointer"
                        >
                          <span>Build Placement Profile</span>
                          <ArrowRight className="h-4.5 w-4.5" />
                        </button>
                      )}
                    </form>

                    {/* In-processing spinner layer */}
                    {(pipelineState === 'processing_phase1' || pipelineState === 'processing_phase2') && (
                      <div className="absolute inset-0 bg-white/90 rounded-none flex flex-col items-center justify-center p-6 text-center z-20">
                        <Loader2 className="h-10 w-10 text-[#111111] animate-spin mb-3" />
                        <p className="text-xs font-mono text-[#111111] font-bold">{loadingText}</p>
                        <p className="text-[10px] text-[#888888] mt-2 font-mono">Running secure audit checkpoints</p>
                      </div>
                    )}

                    {/* Error Message */}
                    {errorMessage && (
                      <div className="mt-4 p-3 border border-[#C8102E] bg-[#FDF2F2] text-[#C8102E] text-xs rounded-none flex items-start gap-2">
                        <AlertTriangle className="h-4 w-4 shrink-0 mt-0.5" />
                        <span>{errorMessage}</span>
                      </div>
                    )}
                  </div>
                </div>

                {/* Right Side: Welcome Description OR HITL Panel */}
                <div className="flex-1 min-w-0">
                  {/* Welcome Screen (Idle State) */}
                  {pipelineState === 'idle' && (
                    <div className="flex-1 flex flex-col justify-center min-h-[450px]" style={{background:'#FFFFFF', border:'1px solid #D9D4C7', padding:'2.5rem'}}>
                      <h2 className="font-serif text-3xl font-bold text-[#111111] mb-4 text-left">
                        Submit your dossier to begin analysis
                      </h2>
                      <hr className="border-[#111111] border-t-2 mb-8" />
                      <p className="font-sans text-sm leading-relaxed text-[#333333] max-w-2xl mb-8">
                        Unlock career insights for campus hiring. Evaluate your resume ATS compatibility, 
                        enrich technical skills via GitHub repositories, match role requirements, and access custom technical/HR preparation timelines.
                      </p>
                      
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full font-sans text-left">
                        <div className="p-5 border border-[#D9D4C7] bg-[#FFFFFF] hover:border-l-[3px] hover:border-l-[#C8102E] transition-all duration-155 rounded-none">
                          <div className="text-[#888888] font-bold text-[10px] uppercase tracking-[0.15em] mb-2">1. Safety First</div>
                          <div className="text-xs leading-relaxed text-[#333333]">Automatic PII scrubbing to hide personal data (Phone/Email/Aadhar) and guard filters.</div>
                        </div>
                        <div className="p-5 border border-[#D9D4C7] bg-[#FFFFFF] hover:border-l-[3px] hover:border-l-[#C8102E] transition-all duration-155 rounded-none">
                          <div className="text-[#888888] font-bold text-[10px] uppercase tracking-[0.15em] mb-2">2. GitHub MCP</div>
                          <div className="text-xs leading-relaxed text-[#333333]">Enriches your resume analysis directly by analyzing codebases and technical stack from GitHub repos.</div>
                        </div>
                        <div className="p-5 border border-[#D9D4C7] bg-[#FFFFFF] hover:border-l-[3px] hover:border-l-[#C8102E] transition-all duration-155 rounded-none">
                          <div className="text-[#888888] font-bold text-[10px] uppercase tracking-[0.15em] mb-2">3. Multi-Agent Flow</div>
                          <div className="text-xs leading-relaxed text-[#333333]">Sequential evaluation, matching fit, and interactive interview question coaching.</div>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Completed Info Banner (when viewing dossier inside completed state) */}
                  {pipelineState === 'completed' && (
                    <div className="flex-1 flex flex-col justify-center min-h-[450px]" style={{background:'#FFFFFF', border:'1px solid #D9D4C7', padding:'2.5rem'}}>
                      <h2 className="font-serif text-3xl font-bold text-[#111111] mb-4 text-left">
                        Dossier Profile Complete
                      </h2>
                      <hr className="border-[#111111] border-t-2 mb-8" />
                      <p className="font-sans text-sm leading-relaxed text-[#333333] max-xl mb-6">
                        You are viewing your submitted parameters. The multi-agent placement evaluation pipeline has finished successfully.
                      </p>
                      <div className="p-4 bg-[#FDF2F2] border-l-[4px] border-[#C8102E] text-xs text-[#333333] space-y-2 mb-8">
                        <span className="font-bold text-[#111111] uppercase tracking-wider block text-[10px]">Active Session Info</span>
                        <div>Target Role: <span className="font-bold">{targetRole}</span></div>
                        <div>GitHub: <span className="font-mono">{githubUsername || 'Not connected'}</span></div>
                        <div>Session ID: <span className="font-mono">{sessionId}</span></div>
                      </div>
                      <button
                        onClick={handleReset}
                        className="py-3 px-6 bg-[#111111] text-[#F7F5F0] text-[11px] uppercase tracking-wider font-semibold hover:bg-[#C8102E] transition-colors w-48 text-center cursor-pointer"
                      >
                        Reset & Build New
                      </button>
                    </div>
                  )}

                  {/* HITL Card State */}
                  {pipelineState === 'pending_hitl' && resumeAnalysis && (
                    <div className="space-y-6">
                      
                      {/* HITL Callout box */}
                      <div 
                        style={{
                          background: '#FFFFFF',
                          borderLeft: '4px solid #C8102E',
                          borderTop: '1px solid #D9D4C7',
                          borderRight: '1px solid #D9D4C7',
                          borderBottom: '1px solid #D9D4C7',
                          padding: '1.5rem'
                        }}
                        className="relative flex flex-col md:flex-row items-center justify-between gap-6 rounded-none"
                      >
                        <div className="flex items-center space-x-4">
                          <div className="h-12 w-12 rounded-none bg-[#FDF2F2] flex items-center justify-center text-[#C8102E] shrink-0">
                            <UserCheck className="h-6 w-6" />
                          </div>
                          <div>
                            <h3 className="font-serif text-lg font-bold text-[#111111]">Human-in-the-Loop Approval Required</h3>
                            <p className="text-xs text-[#888888]">Please review your extracted placement profile below before finalizing matching analysis and interview prep.</p>
                          </div>
                        </div>
                        <div className="flex items-center space-x-3 w-full md:w-auto shrink-0">
                          <button
                            onClick={() => handleHitlApproval(false)}
                            className="flex-1 md:flex-initial py-2.5 px-4 border border-[#111111] bg-white text-[#111111] rounded-none uppercase tracking-wider text-xs font-semibold hover:bg-[#FDF2F2] transition-colors cursor-pointer text-center"
                          >
                            REJECT DRAFT
                          </button>
                          <button
                            onClick={() => handleHitlApproval(true)}
                            className="flex-1 md:flex-initial py-2.5 px-5 bg-[#111111] text-[#F7F5F0] rounded-none uppercase tracking-wider text-xs font-semibold hover:bg-[#C8102E] transition-colors cursor-pointer text-center"
                          >
                            APPROVE EDITION
                          </button>
                        </div>
                      </div>

                      {/* Resume Analysis Summary */}
                      <div 
                        style={{background:'#FFFFFF', border:'1px solid #D9D4C7', padding:'1.5rem'}}
                        className="space-y-6 rounded-none"
                      >
                        <div className="flex items-center justify-between border-b border-[#D9D4C7] pb-4">
                          <div>
                            <h3 className="font-serif text-xl font-bold text-[#111111]">Extracted Placement Profile</h3>
                            <p className="text-[10px] uppercase tracking-[0.15em] text-[#888888] font-sans mt-1">Scrubbed evaluation via ResumeAnalyzerAgent</p>
                          </div>
                          <div className="flex items-center space-x-2 bg-[#F7F5F0] px-3 py-1.5 border border-[#D9D4C7]">
                            <span className="text-[10px] uppercase tracking-[0.15em] text-[#888888] font-sans">ATS Score:</span>
                            <span className="text-lg font-bold font-serif text-[#111111]">
                              {resumeAnalysis.ats_score}/100
                            </span>
                          </div>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                          <div className="space-y-3">
                            <h4 className="text-[10px] uppercase tracking-[0.15em] text-[#888888] font-sans">Extracted Skills</h4>
                            <div className="flex flex-wrap gap-1.5">
                              {resumeAnalysis.extracted_skills?.map((skill, i) => (
                                <span key={i} className="px-2 py-0.5 text-[11px] bg-white border border-[#D9D4C7] text-[#111111] rounded-none">
                                  {skill}
                                </span>
                              ))}
                            </div>
                          </div>

                          <div className="space-y-3">
                            <h4 className="text-[10px] uppercase tracking-[0.15em] text-[#C8102E] font-sans">Missing Target Skills</h4>
                            <div className="flex flex-wrap gap-1.5">
                              {resumeAnalysis.missing_skills?.map((skill, i) => (
                                <span key={i} className="px-2 py-0.5 text-[11px] border border-[#C8102E] text-[#C8102E] rounded-none">
                                  {skill}
                                </span>
                              ))}
                            </div>
                          </div>
                        </div>

                        <div className="space-y-3 pt-2">
                          <h4 className="text-[10px] uppercase tracking-[0.15em] text-[#888888] font-sans">Actionable Improvements</h4>
                          <ul className="space-y-2 text-sm text-[#333333] list-disc list-inside font-sans">
                            {resumeAnalysis.suggestions?.map((sug, i) => (
                              <li key={i} className="leading-relaxed">{sug}</li>
                            ))}
                          </ul>
                        </div>

                        {githubSummary && (
                          <div className="p-4 bg-[#F7F5F0] border border-[#D9D4C7] space-y-2">
                            <h4 className="text-[10px] uppercase tracking-[0.15em] text-[#111111] flex items-center gap-1.5 font-sans">
                              <Github className="h-3.5 w-3.5" /> Enriched GitHub Repositories Info
                            </h4>
                            <pre className="text-[11px] text-[#333333] font-mono whitespace-pre-wrap leading-relaxed max-h-36 overflow-y-auto">
                              {githubSummary}
                            </pre>
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Dashboard States when completed */}
            {pipelineState === 'completed' && activeTab !== 'dossier' && (
              <div className="space-y-6 flex-1 flex flex-col min-h-0">
                
                {/* Profile Details Top Info */}
                <div 
                  style={{background:'#FFFFFF', border:'1px solid #D9D4C7', padding:'1.25rem'}}
                  className="flex items-center justify-between rounded-none"
                >
                  <div>
                    <h3 className="font-serif text-lg font-bold text-[#111111] flex items-center gap-2">
                      <CheckCircle className="h-4.5 w-4.5 text-[#111111]" /> Placement Package Generated
                    </h3>
                    <p className="text-[11px] text-[#888888] font-mono mt-1">
                      TARGET ROLE: <span className="text-[#111111] font-bold">{targetRole.toUpperCase()}</span> | SESSION: {sessionId.substring(0,8).toUpperCase()}
                    </p>
                  </div>
                  <div className="flex items-center space-x-4">
                    <div className="flex items-center space-x-2">
                      <span className="text-[10px] uppercase tracking-[0.15em] text-[#888888] font-sans">ATS Score:</span>
                      <span className="font-serif text-lg font-bold text-[#111111]">{resumeAnalysis?.ats_score}%</span>
                    </div>
                    {jobMatch && (
                      <div className="flex items-center space-x-2">
                        <span className="text-[10px] uppercase tracking-[0.15em] text-[#888888] font-sans">Match:</span>
                        <span className="font-serif text-lg font-bold text-[#C8102E]">{jobMatch.match_percentage}%</span>
                      </div>
                    )}
                  </div>
                </div>

                {/* Dashboard Tab Panels */}
                <div className="flex-1 min-h-0">
                  
                  {/* 1. Resume Panel */}
                  {activeTab === 'resume' && resumeAnalysis && (
                    <div 
                      style={{background:'#FFFFFF', border:'1px solid #D9D4C7', padding:'1.5rem'}}
                      className="space-y-6 animate-fade-in rounded-none"
                    >
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div className="space-y-4">
                          <div className="space-y-1.5">
                            <h4 className="text-[10px] uppercase tracking-[0.15em] text-[#888888] font-sans">ATS Placement Score</h4>
                            <div className="flex items-baseline space-x-2">
                              <span className="text-8xl font-bold text-[#111111] font-serif">{displayAts}</span>
                              <span className="text-[#888888] text-lg">/100</span>
                            </div>
                            <p className="text-sm leading-relaxed text-[#333333]">
                              Compatibility evaluated based on tech stack relevance, project depth, metrics verification, and college parameters.
                            </p>
                          </div>

                          <div className="space-y-2 pt-2">
                            <h4 className="text-[10px] uppercase tracking-[0.15em] text-[#888888] font-sans">Found Skills ({resumeAnalysis.extracted_skills?.length || 0})</h4>
                            <div className="flex flex-wrap gap-1.5">
                              {resumeAnalysis.extracted_skills?.map((skill, i) => (
                                <span key={i} className="px-2 py-0.5 text-[11px] bg-[#111111] text-[#F7F5F0] rounded-none">
                                  {skill}
                                </span>
                              ))}
                            </div>
                          </div>
                        </div>

                        <div className="space-y-4">
                          <div className="space-y-2">
                            <h4 className="text-[10px] uppercase tracking-[0.15em] text-[#C8102E] font-sans">Missing Core Skills</h4>
                            <div className="flex flex-wrap gap-1.5">
                              {resumeAnalysis.missing_skills?.map((skill, i) => (
                                <span key={i} className="px-2 py-0.5 text-[11px] border border-[#C8102E] text-[#C8102E] rounded-none">
                                  {skill}
                                </span>
                              ))}
                            </div>
                          </div>

                          <div className="space-y-2 pt-2">
                            <h4 className="text-[10px] uppercase tracking-[0.15em] text-[#888888] font-sans">Improvement Steps</h4>
                            <ul className="space-y-2 text-sm text-[#333333] list-disc list-inside font-sans">
                              {resumeAnalysis.suggestions?.map((sug, i) => (
                                <li key={i} className="leading-relaxed">{sug}</li>
                              ))}
                            </ul>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* 2. Job Alignment Panel */}
                  {activeTab === 'matcher' && jobMatch && (
                    <div 
                      style={{background:'#FFFFFF', border:'1px solid #D9D4C7', padding:'1.5rem'}}
                      className="space-y-6 animate-fade-in rounded-none"
                    >
                      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 border-b border-[#D9D4C7] pb-6">
                        <div className="space-y-1.5">
                          <h4 className="text-[10px] uppercase tracking-[0.15em] text-[#888888] font-sans">Job Match Percentage</h4>
                          <div className="flex items-baseline space-x-2">
                            <span className="text-7xl font-bold text-[#C8102E] font-serif">{displayMatch}%</span>
                          </div>
                          <p className="text-sm leading-relaxed text-[#333333]">Alignment of your background with the target position's core requirements.</p>
                        </div>

                        {/* Custom progress bar */}
                        <div className="w-full md:w-60 bg-[#F7F5F0] p-4 border border-[#D9D4C7] rounded-none">
                          <div className="text-[10px] uppercase tracking-wider font-mono text-[#888888] mb-1">Fit Level</div>
                          <div className="h-2 w-full bg-[#D9D4C7] overflow-hidden">
                            <div 
                              className="h-full bg-[#111111] transition-all duration-1000"
                              style={{ width: `${jobMatch.match_percentage}%` }}
                            />
                          </div>
                          <div className="flex justify-between text-[10px] text-[#888888] mt-1 font-mono">
                            <span>0%</span>
                            <span>{jobMatch.match_percentage >= 75 ? 'Strong Match' : jobMatch.match_percentage >= 50 ? 'Medium Match' : 'Low Match'}</span>
                            <span>100%</span>
                          </div>
                        </div>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div className="space-y-3">
                          <h4 className="text-[10px] uppercase tracking-[0.15em] text-[#888888] font-sans">Matched Competencies</h4>
                          {jobMatch.matched_skills?.length > 0 ? (
                            <div className="flex flex-wrap gap-1.5">
                              {jobMatch.matched_skills.map((skill, i) => (
                                <span key={i} className="px-2 py-0.5 text-[11px] bg-[#111111] text-[#F7F5F0] rounded-none">
                                  {skill}
                                </span>
                              ))}
                            </div>
                          ) : (
                            <p className="text-xs text-[#888888] italic">No direct matching skills identified.</p>
                          )}
                        </div>

                        <div className="space-y-3">
                          <h4 className="text-[10px] uppercase tracking-[0.15em] text-[#C8102E] font-sans">Critical Keywords Missing</h4>
                          {jobMatch.missing_skills?.length > 0 ? (
                            <div className="flex flex-wrap gap-1.5">
                              {jobMatch.missing_skills.map((skill, i) => (
                                <span key={i} className="px-2 py-0.5 text-[11px] border border-[#C8102E] text-[#C8102E] rounded-none">
                                  {skill}
                                </span>
                              ))}
                            </div>
                          ) : (
                            <p className="text-xs text-[#888888] italic">No critical gaps identified.</p>
                          )}
                        </div>
                      </div>

                      <div className="p-4 bg-[#F7F5F0] border border-[#D9D4C7] space-y-2 rounded-none">
                        <h4 className="text-[10px] uppercase tracking-[0.15em] text-[#111111] font-sans">Requirement Gap Analysis</h4>
                        <p className="text-sm leading-relaxed text-[#333333] font-sans">
                          {jobMatch.gap_analysis}
                        </p>
                      </div>
                    </div>
                  )}

                  {/* 3. Prep Coach Panel */}
                  {activeTab === 'prep' && interviewPrep && (
                    <div className="space-y-6 animate-fade-in">
                      
                      {/* Technical and HR split */}
                      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
                        
                        {/* Tech prep questions */}
                        <div 
                          style={{background:'#FFFFFF', border:'1px solid #D9D4C7', padding:'1.5rem'}}
                          className="space-y-4 rounded-none"
                        >
                          <h4 className="font-serif text-lg font-bold text-[#111111] flex items-center gap-1.5 border-b border-[#D9D4C7] pb-2">
                            <Award className="h-4.5 w-4.5 text-[#111111]" /> Technical Questions
                          </h4>
                          <div className="space-y-3 max-h-[350px] overflow-y-auto pr-2">
                            {interviewPrep.technical_questions?.map((q, i) => (
                              <div key={i} className="p-3.5 bg-[#F7F5F0] border border-[#D9D4C7] space-y-1.5 text-xs rounded-none">
                                <div className="flex items-center justify-between">
                                  <span className="px-2 py-0.5 text-[9px] font-bold font-sans uppercase bg-[#111111] text-[#F7F5F0] rounded-none">
                                    {q.topic}
                                  </span>
                                </div>
                                <p className="font-serif font-bold text-[#111111] text-sm">Q: {q.question}</p>
                                <p className="text-[#333333] italic text-xs font-sans">Tip: {q.tips}</p>
                              </div>
                            ))}
                          </div>
                        </div>

                        {/* HR Questions */}
                        <div 
                          style={{background:'#FFFFFF', border:'1px solid #D9D4C7', padding:'1.5rem'}}
                          className="space-y-4 rounded-none"
                        >
                          <h4 className="font-serif text-lg font-bold text-[#111111] flex items-center gap-1.5 border-b border-[#D9D4C7] pb-2">
                            <HelpCircle className="h-4.5 w-4.5 text-[#111111]" /> Placement HR Questions
                          </h4>
                          <div className="space-y-3 max-h-[350px] overflow-y-auto pr-2">
                            {interviewPrep.hr_questions?.map((q, i) => (
                              <div key={i} className="p-3.5 bg-[#F7F5F0] border border-[#D9D4C7] space-y-1.5 text-xs rounded-none">
                                <p className="font-serif font-bold text-[#111111] text-sm">Q: {q.question}</p>
                                <div className="text-xs text-[#333333] font-sans">
                                  <span className="text-[#111111] font-bold uppercase tracking-wider text-[10px]">Recruiter Intent:</span> {q.rationale}
                                </div>
                                <div className="text-xs text-[#333333] font-sans mt-1">
                                  <span className="text-[#111111] font-bold uppercase tracking-wider text-[10px]">Strategy:</span> {q.strategy}
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>

                      </div>

                      {/* Study Timeline Plan */}
                      <div 
                        style={{background:'#FFFFFF', border:'1px solid #D9D4C7', padding:'1.5rem'}}
                        className="space-y-4 rounded-none"
                      >
                        <h4 className="font-serif text-lg font-bold text-[#111111] flex items-center gap-1.5 border-b border-[#D9D4C7] pb-2">
                          <BookOpen className="h-4.5 w-4.5 text-[#111111]" /> Placement Prep Study Plan
                        </h4>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                          {interviewPrep.study_plan?.map((day, i) => (
                            <div key={i} className="p-4 bg-[#FFFFFF] border border-[#D9D4C7] rounded-none space-y-2 text-xs">
                              <div className="font-bold text-[#C8102E] font-serif text-2xl">{day.day}</div>
                              <div className="font-serif font-bold text-[#111111] border-b border-[#D9D4C7] pb-1.5 text-sm">{day.focus}</div>
                              <ul className="space-y-1.5 text-[#333333] font-sans list-disc list-inside">
                                {day.tasks?.map((task, idx) => (
                                  <li key={idx} className="leading-relaxed text-xs">{task}</li>
                                ))}
                              </ul>
                            </div>
                          ))}
                        </div>
                      </div>

                    </div>
                  )}

                </div>
              </div>
            )}

          </div>
        </main>
      </div>

      {/* Terminal Audit Drawer (Slide Up Drawer) */}
      <div 
        className={`fixed bottom-0 left-0 right-0 z-50 bg-[#111111] transition-all duration-350`}
        style={{
          borderTop: '1px solid #333333',
          height: isAuditOpen ? '360px' : '44px'
        }}
      >
        {/* Toggle Bar */}
        <div 
          onClick={() => setIsAuditOpen(!isAuditOpen)}
          className="w-full py-2.5 px-6 flex items-center justify-between border-b border-[#333333] bg-[#111111] cursor-pointer select-none"
        >
          <div className="flex items-center space-x-2 text-[11px] font-mono text-[#F7F5F0]">
            <Shield className="h-4 w-4 text-[#F7F5F0]" />
            <span className="font-bold tracking-[0.2em] text-[10px] uppercase">SECURITY LOG</span>
            <span className="text-[10px] bg-[#333333] px-2 py-0.5 border border-[#444444] ml-2 rounded-none">
              {auditLogs.length} events logged
            </span>
          </div>
          <div className="text-[#888888] hover:text-[#F7F5F0] transition-colors">
            {isAuditOpen ? <ChevronDown className="h-4.5 w-4.5" /> : <ChevronUp className="h-4.5 w-4.5" />}
          </div>
        </div>

        {/* Audit terminal drawer content */}
        <div className="p-5 overflow-y-auto h-[310px] font-mono text-[11px] bg-[#111111] text-[#F7F5F0]">
          <div className="space-y-2 max-w-7xl mx-auto">
            {auditLogs.length === 0 ? (
              <div className="text-[#888888] italic py-8 text-center">No system events logged yet. Execute an orchestration to run audits.</div>
            ) : (
              auditLogs.map((log, idx) => {
                let statusColor = "text-[#F7F5F0]";
                if (log.status === "REDACTED" || log.status === "BLOCKED" || log.status === "WARNING") {
                  statusColor = "text-[#fbbf24] font-semibold";
                } else if (log.status === "SUCCESS" || log.status === "CLEAN" || log.status === "PASSED" || log.status === "APPROVED") {
                  statusColor = "text-[#4ade80]";
                } else if (log.status === "ERROR" || log.status === "EXCEPTION") {
                  statusColor = "text-[#f87171] font-bold";
                }
                
                const time = new Date(log.timestamp).toLocaleTimeString();
                
                return (
                  <div key={idx} className="flex items-start space-x-3 p-1.5 hover:bg-[#333333]/40 transition-colors">
                    <span className="text-[#888888] shrink-0 select-none">[{time}]</span>
                    <span className="text-[#888888] font-bold uppercase tracking-wider shrink-0 select-none">{log.action}:</span>
                    <span className={`shrink-0 select-none ${statusColor}`}>[{log.status}]</span>
                    <span className="text-[#F7F5F0] flex-1 truncate">{JSON.stringify(log.details)}</span>
                  </div>
                );
              })
            )}
          </div>
        </div>
      </div>

    </div>
  );
}
"""

with open(app_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find the exact line index for "return (" after handleReset
reset_idx = -1
for i, line in enumerate(lines):
    if "const handleReset =" in line:
        reset_idx = i
        break

if reset_idx == -1:
    print("Error: Could not locate handleReset")
    exit(1)

target_idx = -1
for i in range(reset_idx, len(lines)):
    if "return (" in lines[i]:
        target_idx = i
        break

if target_idx == -1:
    print("Error: Could not locate return statement")
    exit(1)

# Truncate lines from target_idx to the end and append new part
restructured_lines = lines[:target_idx]
restructured_content = "".join(restructured_lines) + new_code_part

with open(app_path, "w", encoding="utf-8") as f:
    f.write(restructured_content)

print("App.jsx restructured successfully!")
