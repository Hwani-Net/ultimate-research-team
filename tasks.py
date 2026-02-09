from crewai import Task
import re

class UltimateResearchTasks:
    """
    Tier-1 Strategy Firm Workflow (v2.0)
    - Source Validation
    - Quant-X Visualization
    - Dialectic Debate
    - Business Logic (Profit/Workflow)
    """
    
    def initial_research_task(self, agent, topic, image_data=None):
        vision_instruction = ""
        if image_data:
            vision_instruction = f"""
            [VISION INTELLIGENCE ACTIVE]
            Analyze the attached image context:
            1. Describe key visual elements.
            2. Connect these elements to the topic '{topic}'.
            3. Find external data that validates this visual evidence.
            """

        return Task(
            description=f"""Conduct DEEP & VALIDATED web research based on the exact USER COMMAND below:
            
            USER COMMAND: "{topic}"
            
            [VISION INTELLIGENCE]: {vision_instruction}

            [PROTOCOL: SOURCE AUDITOR ACTIVE]
            - YOU MUST click and verify every link.
            - If a page is 404 or low quality, DISCARD it instantly.
            - Only keep "Golden Sources" (Official Docs, Tier-1 News, Academic Papers).

            [RESEARCH TARGETS]
            1. Latest Market Data (2025-2026 Focus)
            2. Competitor Moves & Hidden Strategies
            3. Technical Specs / Pricing / Revenue Models
            
            OUTPUT FORMAT:
            - List of Verified Facts with [Source URL]
            - "Golden Source" Verification Status (e.g., "Link Active: Yes")
            """,
            expected_output="""A validated dossier of facts. source links must be tested and confirmed alive.
            Focus on hard numbers and strategic moves.""",
            agent=agent,
        )

    def data_visualization_task(self, agent):
        return Task(
            description="""[QUANT-X ACTIVATED]
            Review the research findings. Extract ALL numerical data (Revenue, Growth %, Market Size).
            
            1. Create a Markdown Table summarizing key financial/usage metrics.
            2. Generate 'Mermaid.js' code for:
               - A Pie Chart (Market Share or Cost Breakdown)
               - A Bar configuration (Growth/Comparison)
               - A Sequence Diagram (if process-related)
            
            DO NOT output images. Output the CODE blocks for Mermaid.
            """,
            expected_output="""Markdown tables and valid Mermaid.js code blocks. 
            No vague text. Only Numbers and Charts.""",
            agent=agent,
        )

    def debate_task(self, agent):
        return Task(
            description="""[THE DIALECTIC ARENA]
            Initiate a debate between two personas regarding the research findings from the USER COMMAND above:
            
            1. THE OPTIMIST (Silicon Valley VC): "This is the next trillion-dollar opportunity!"
            2. THE PESSIMIST (Risk Officer): "Regulatory hell, tech bubble, and safety risks."
            
            Conduct 3 rounds of argument.
            Round 1: Market Potential vs. Bubble Risk
            Round 2: Technical Feasibility vs. Physical Constraints
            Round 3: Social Impact vs. Backlash
            
            Synthesize the winner's logic into a 'Risk Assessment Matrix'.
            """,
            expected_output="""Transcript of the 3-round debate and a Final Risk Assessment Matrix.
            Highlight the 'Killer Arguments' that won.""",
            agent=agent,
        )

    def business_logic_task(self, agent):
        return Task(
            description="""[MBB STRATEGY MODULE]
            Based on the research and debate, generate:
            
            1. **Profitability Prediction Model**:
               - Estimate TAM (Total Addressable Market) / SAM / SOM in USD.
               - Predict ROI timeline (Break-even point).
               - Identify 3 high-margin revenue streams.
               
            2. **Investment Defense & Risk Hedge**:
               - Create a "Risk Hedge Report" for potential investors.
               - Analysis of regulatory risks (Global & Local).

            3. **Execution Workflow (The "How-To")**:
               - Create a Step-by-Step Implementation Plan (Phase 1 to Phase 4).
               - Define Key Milestones & KPIs.
               - Generate a Mermaid.js GANTT Chart code for this timeline.
            """,
            expected_output="""Financial projections (TAM/SAM/SOM), Risk Hedge Report, and a detailed Execution Plan.""",
            agent=agent,
        )

    def final_report_task(self, agent, topic):
        # Dynamic Korean filename generation
        safe_topic = re.sub(r'[^\w\s-]', '', topic).strip()
        safe_topic = re.sub(r'[-\s]+', '_', safe_topic)
        if not safe_topic:
            safe_topic = "Strategic_Report"
        
        filename = f"Strategy_Report_{safe_topic[:40]}.md"
            
        return Task(
            description=f"""Synthesize ALL previous outputs into the 'Ultimate Strategic Report' for '{topic}'.
            
            [STRUCTURE]
            1. **Executive Dashboard**:
               - 3-Line High-level Summary.
               - [Quant-X] Insert the key Markdown Tables here.
            
            2. **Visual Intelligence & Charts**:
               - Render the Mermaid.js Charts (Pie/Bar) from the Data Analyst.
               - Explain the insights derived from these charts.
            
            3. **The Dialectic Arena (Risk Analysis)**:
               - Summarize the Optimist vs. Pessimist debate.
               - Present the 'Risk Assessment Matrix'.
            
            4. **Strategic Execution & Investment Defense**:
               - [Business Consultant Output] Insert the Profitability Model.
               - **Risk Hedge Strategy**: How to protect investor capital.
               - Display the Execution Workflow & Mermaid Gantt Chart.
               
            5. **Korean Executive Summary (한국어 요약 및 제언)**:
               - Translate the core insights into perfect professional Korean.
               - **[K-Compliance Check]**: 
                 verify compliance with 'Data 3 Laws' (Credit/Personal/Network Act) for the Korean market.
               - Add a specific section: "To-Do List for Korean Market Entry".
             
            [FORMATTING]
            - Use ````mermaid` blocks for charts.
            - Use bolding for key financial figures.
            - Tone: MBB Senior Partner (McKinsey/Bain/BCG).
            
            [SOULLESS MODE v11.0 CHECK]
            Include the JSON self-evaluation block at the very end.
            """,
            expected_output="""A Masterpiece Report containing text, tables, mermaid charts, debate summaries, and financial models. 
            Bilingual (English Main + Korean Summary).""",
            agent=agent,
            output_file=filename,
        )


# ============================================================================
# NEW: BOARD OF DIRECTORS TASKS
# ============================================================================

class BoardTasks:
    """
    Strategic Board Meeting Tasks
    """
    
    def kill_switch_task(self, clo, researcher, project_idea):
        """
        Pre-Board Kill Switch: Sanitation Layer Only (Board Directive 2026-02-09)
        
        Purpose: Filter out OBVIOUS fatal flaws that waste Board time.
        Philosophy: "Sanitation, not Strategy" - Binary checks only.
        """
        return Task(
            description=f"""[KILL SWITCH PROTOCOL - SANITATION LAYER ONLY]
            
            Project Proposal: "{project_idea}"
            
            **BOARD DIRECTIVE (2026-02-09):**
            The Kill Switch is NOT a strategic filter. It is a sanitation check.
            Only KILL if the flaw is 100% obvious and non-negotiable.
            
            **HARD GATE #1: Illegal Activities (CLO)**
            - Is this activity illegal under US/International law?
            - Examples: Drug trafficking, weapon sales, child exploitation, financial fraud
            - Check: Does the core business model violate federal criminal statutes?
            → KILL if: Core activity is criminal offense
            
            **HARD GATE #2: Identical Trademark Collision (CLO)**
            - Is the project name EXACTLY IDENTICAL to a registered trademark?
            - Criteria: EXACT string match only (not similar, not confusingly similar)
            - Examples to KILL: "Google", "Apple", "Microsoft", "Notion" (exact)
            - Examples to PASS: "Notion AI+", "Apple-Like UI", "Google Clone" (not exact)
            → KILL if: Exact name match to active trademark in Class 9/35/42
            
            **HARD GATE #3: Coherence Check (Researcher)**
            - Does this proposal make logical sense?
            - Is this a hallucination or gibberish? (e.g., "Build a time machine using bananas")
            - Can a human understand what this project aims to do?
            → KILL if: Proposal lacks coherent logic or syntax
            
            **HARD GATE #4: Zero Total Addressable Market (Researcher)**
            - Is the target market literally zero people?
            - Examples: "App for dinosaurs", "Service for people who don't exist"
            - Note: Niche markets (100 people) are OK. Zero is not.
            → KILL if: TAM = 0 (literally no potential customers globally)
            
            **CRITICAL RULES:**
            1. If there's ANY debate ("maybe", "it depends"), DO NOT KILL. Let Board decide.
            2. Red Ocean? → Not your problem. Board will debate differentiation.
            3. Similar trademark? → Not your problem. Board will debate rebranding.
            4. Technical difficulty? → Not your problem. Board will debate resources.
            
            **OUTPUT REQUIREMENTS:**
            You MUST return ONE of these two formats:
            
            1. **PASS Decision**:
               "✅ KILL SWITCH: PASS
               - Gate 1 (Illegal): CLEAR
               - Gate 2 (Trademark): CLEAR
               - Gate 3 (Coherence): CLEAR
               - Gate 4 (TAM): CLEAR
               → Proceeding to Board Meeting"
            
            2. **KILL Decision** (ONLY if 100% obvious):
               "🛑 KILL SWITCH: KILL
               - Gate Failed: [Number and name]
               - Reason: [Specific fatal flaw]
               - Evidence: [Concrete proof]
               - Note: This is a sanitation check, not a strategic rejection."
            
            **REMEMBER**: Your job is SANITATION, not STRATEGY. When in doubt, PASS.
            """,
            expected_output="PASS or KILL decision with specific gate that failed",
            agent=clo,  # CLO leads sanitation
        )
    
    def strategy_session_task(self, ceo, cfo, cto, cmo, clo, project_idea):
        """Initial ideation and validation"""
        return Task(
            description=f"""[BOARD OF DIRECTORS: STRATEGY SESSION]
            
            Project Proposal: "{project_idea}"
            
            [MANDATORY PHASE 0: BRAND & MARKET VIABILITY]
            Before individual assessments, the CLO and CMO must jointly report on:
            1. Trademark availability (KIPRIS/Global)
            2. App Store/Market existence
            3. Domain (.com, .io, .co.kr) availability
            YOU MUST start the report with: "Phase 0: Brand Validation PASSED" (or FAILED).
            
            [STRATEGIC ASSESSMENT]
            Each board member must provide their perspective:
            
            [CEO - Vision Architect]:
            - Does this solve a real, urgent problem?
            - What's the unique moat or differentiation?
            - 10-year vision: Where could this go?
            
            [CFO - Risk & ROI Analyst]:
            - Preliminary cost estimate (Dev + Marketing + Operations)
            - Revenue model potential (SaaS? One-time? Usage-based?)
            - Break-even timeline estimate
            
            [CTO - Tech Strategist]:
            - Technical feasibility (1-10 scale)
            - Recommended tech stack
            - Scalability concerns or architecture risks
            
            [CMO - Market Expert]:
            - Target user persona (Who needs this?)
            - Top 3 competitors and their weaknesses
            - GTM (Go-To-Market) channel recommendation
            
            [CLO - Legal Officer]:
            - Regulatory risks (GDPR, CCPA, AI Act, etc.)
            - Data privacy concerns
            - IP/licensing risks
            
            OUTPUT FORMAT:
            Create a "Detailed Board Meeting Transcript" that captures the LIVE DEBATE.
            - **SPEAKER FORMAT**: Always use "Role [Model Name]" (e.g., **CEO [Gemini 3 Ultra]**: ...)
            - Show the back-and-forth arguments.
            - Highlights where members disagreed and how they resolved it.
            - End with a GO/NO-GO recommendation and the final Minutes summary.
            """,
            expected_output="""A vivid Board Meeting Transcript showing the debate process with strict Model Name attribution, followed by the official Minutes and Decision.""",
            agent=ceo,  # CEO leads the meeting
        )
    
    def approval_task(self, ceo, strategy_minutes):
        """Final approval decision"""
        return Task(
            description=f"""[CEO FINAL DECISION]
            
            Review the Board Meeting Minutes:
            {strategy_minutes}
            
            Make the final call:
            - **APPROVED**: Green-light the project with specific conditions/guardrails
            - **REJECTED**: Kill the project with clear reasoning
            - **REVISE**: Request specific changes before re-submission
            
            If APPROVED, outline the Top 3 Success Criteria for the Project Team.
            """,
            expected_output="""Final decision (APPROVED/REJECTED/REVISE) with rationale and success criteria.""",
            agent=ceo,
        )
    
    def emergency_consultation_task(self, ceo, cfo, cto, cmo, clo, blocker_description):
        """Emergency problem-solving consultation"""
        return Task(
            description=f"""[EMERGENCY BOARD MEETING]
            
            The Project Team has encountered a critical blocker:
            "{blocker_description}"
            
            Each board member must provide a solution recommendation:
            
            [CEO]: Strategic pivot options
            [CFO]: Budget reallocation or cost-cutting measures
            [CTO]: Technical workarounds or architecture changes
            [CMO]: Market positioning adjustments
            [CLO]: Legal/compliance mitigation strategies
            
            Synthesize the debate: Who argued for what? Who compromised?
            Output the full TRANSCRIPT of the discussion.
            """,
            expected_output="""A real-time debate log showing the clash of ideas between executives, leading to a final consensus.""",
            agent=ceo,
        )


# ============================================================================
# NEW: PROJECT TEAM TASKS
# ============================================================================

class ProjectTeamTasks:
    """
    Execution Squad Tasks
    """
    
    def planning_task(self, pm, approved_strategy):
        """Create implementation workflow"""
        return Task(
            description=f"""[PROJECT MANAGER: IMPLEMENTATION PLANNING]
            
            Based on the approved Board strategy:
            {approved_strategy}
            
            Create a detailed implementation plan:
            
            1. **Task Breakdown**:
               - Break the project into 10-15 granular tasks
               - Assign each task to a team member (Designer, Backend, Frontend, QA)
               - Identify dependencies (Task X must complete before Task Y)
            
            2. **Timeline**:
               - Estimate effort for each task (hours/days)
               - Create a Mermaid Gantt chart
               - Identify the critical path
            
            3. **Risk Mitigation**:
               - List top 3 execution risks
               - Contingency plans for each
            
            OUTPUT: Create a task.md file with detailed workflow.
            """,
            expected_output="""task.md file with complete task breakdown, timeline, and risk mitigation plan.""",
            agent=pm,
            output_file="task.md",
        )
    
    def blueprint_creation_task(self, backend, frontend, designer, qa, implementation_plan):
        """Design the GRAVITY AI BLUEPRINT"""
        return Task(
            description=f"""[ARCHITECT SQUAD: GRAVITY AI BLUEPRINT CREATION]
            
            Implementation Plan:
            {implementation_plan}
            
            Instead of writing code, create a comprehensive **"Implementation Blueprint"** for Gravity AI (the user's local AI) to execute.
            
            [OBJECTIVE]
            Write a single file `blueprint.md` that contains instructions for creating every single file in the project.
            
            [STRUCTURE OF BLUEPRINT.MD]
            1. **File Tree**: Complete directory structure.
            2. **File Specifications** (Iterate through every file):
               - **File Path**: e.g., `src/main.py`
               - **Purpose**: What this file does.
               - **Core Logic**: Pseudo-code or step-by-step logic description.
               - **Key Functions/Classes**: Signatures and responsibilities.
               - **Dependencies**: Libraries required.
               - **[MANDATORY]**: Any specific critical instructions (e.g., "Use CORS middleware", "Set button color to #FF00FF").
            
            [ROLE INSTRUCTIONS]
            - **Backend Architect**: Define Schema, API Routes, Pydantic models (Do not write full implementation).
            - **Frontend Architect**: Define Component props, State logic, Tailwind classes.
            - **Designer**: Define Color Tokens and Layout Grid.
            - **QA**: Define "Critical Test Cases" that Gravity AI must verify.
            
            [OUTPUT GUARANTEE]
            The output MUST be a valid Markdown file named `blueprint.md`.
            It must be so detailed that a dumb AI could copy-paste it into a perfect app.
            """,
            expected_output="""A `blueprint.md` file containing the Master Architectural Specification for Gravity AI.""",
            agent=backend,  # Backend leads the architecture
            output_file="blueprint.md"
        )
