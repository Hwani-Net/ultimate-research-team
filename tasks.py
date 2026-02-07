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
