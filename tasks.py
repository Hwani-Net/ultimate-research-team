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

from crewai import Task, Agent
from models import KillSwitchResult, BoardDecision

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
            
            **OUTPUT FORMAT:**
            Return a JSON object with these fields:
            - decision: "PASS" or "KILL"
            - gate_failed: Gate number (1-4) or null if PASS
            - gate_name: Name of failed gate or null
            - reason: Detailed explanation
            - evidence: Concrete proof (trademark ID, law citation) or null
            
            **REMEMBER**: Your job is SANITATION, not STRATEGY. When in doubt, PASS.
            """,
            expected_output="Structured decision with gate analysis",
            agent=clo,  # CLO leads sanitation
            output_pydantic=KillSwitchResult  # ← Structured output enforcement
        )
    
    def strategy_session_task(self, ceo, cfo, cto, cmo, clo, project_idea):
        """Execute Strategic Computation Protocol"""
        return Task(
            description=f"""[SYSTEM PROTOCOL: STRATEGY OPTIMIZATION]
            
            Input Proposal: "{project_idea}"
            
            [OPERATIONAL DIRECTIVE]
            Perform multi-variable optimization to determine project viability.
            Do NOT "debate". "Calculate" the optimal path.
            
            [COMPUTATION MODULES]
            1. [Kill Switch Check]:
               - [Compliance Filter]: Check Regulatory Constraints (True/False).
               - [Signal Processor]: Check Market Existence (Red/Blue Ocean).
               -> IF (Compliance == False) OR (Market == Saturated) -> TERMINATE.
            
            2. [Variable Estimation]:
               - [Vision Optimizer]: Estimate LTV (Lifetime Value).
               - [Resource Allocator]: Estimate CAC (Customer Acquisition Cost) & Burn Rate.
               - [Feasibility Probabilist]: Estimate P(Success).
            
            3. [Decision Matrix Calculation]:
               - Score = (LTV - CAC) * P(Success) / Risk_Factor
            
            [OUTPUT FORMAT: Strategic_Matrix.md]
            The output must be a structured decision log.
            
            Structure:
            # STRATEGIC COMPUTATION LOG
            
            ## 1. Boolean Gates
            - Legal Compliance: [TRUE/FALSE]
            - Tech Feasibility: [> 80%?]
            
            ## 2. Variable Analysis (Data Injection)
            - **Market Signal**: [Niche/Mass/Ghost]
            - **Unit Economics**: LTV $[X] vs CAC $[Y]
            - **Tech Complexity**: [O(1) to O(N^2) scale]
            
            ## 3. Conflict Resolution
            - [Constraint Detected] -> [Optimization Applied]
            (e.g., "High Cost" -> "Switch to Serverless")
            
            ## 4. Final Computation
            - **Decision**: [GO / NO-GO / PIVOT]
            - **Confidence Score**: [0.0 - 1.0]
            """,
            expected_output="""A `Strategic_Matrix.md` file containing the calculated decision logic and final probability score.""",
            agent=ceo,  # Vision Optimizer leads the computation
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
        """Execute Architecture Compilation Protocol"""
        return Task(
            description=f"""[SYSTEM PROTOCOL: ARCHITECTURE COMPILATION]
            
            Input: Strategic Implementation Plan
            {implementation_plan}
            
            [OPERATIONAL DIRECTIVE]
            Execute parallel processing to generate the [GRAVITY AI BLUEPRINT].
            Do NOT "discuss". "Compute" the optimal solution.
            
            [MODULE ASSIGNMENTS]
            1. [Logic Unit]: Generate Schema, API Specs, and Auth Logic. Target: O(1) complexity.
            2. [Interface Unit]: Define Component Atoms, State Graph, and Hydration Strategy.
            3. [Visualizer]: Generate Design Tokens (JSON) and Layout Grid System.
            4. [Validator]: Simulate 1M concurrent users. Identify bottlenecks.
            
            [DATA FLOW]
            Visualizer -> tokens.json -> Interface Unit
            Logic Unit -> api_spec.yaml -> Interface Unit
            Validator -> stress_test_report -> Logic Unit (Optimize)
            
            [CONFLICT RESOLUTION ALGORITHM]
            If [Visualizer] output increases [Logic Unit] latency > 50ms:
            -> REJECT Visualizer output.
            -> Visualizer MUST re-render with simplified shaders.
            
            [OUTPUT FORMAT: blueprint.md]
            The output must be a machine-readable directive file.
            
            Structure:
            # GRAVITY AI BLUEPRINT (v2026.02)
            
            ## 1. System Manifest
            - Stack: [Precision Defined Technologies]
            - Architecture: [Monolith/Microservices/Serverless]
            
            ## 2. File Directive (Iterate All)
            ### `/src/core/engine.py`
            - **Logic**: [Step-by-step algorithm]
            - **Complexity**: O(N) or O(1)
            - **Dependencies**: [Libs]
            
            ## 3. Security Protocol
            - Auth: [Strategy]
            - Encryption: [Algorithm]
            
            ## 4. Conflict Log
            - [Conflict Detected] -> [Resolution Applied]
            """,
            expected_output="""A `blueprint.md` file containing the Master Architectural Specification for Gravity AI, written in strict technical directive format.""",
            agent=backend,  # Logic Unit leads the architecture
            output_file="blueprint.md"
        )
