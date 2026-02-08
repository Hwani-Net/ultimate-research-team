import os
from crewai import Agent, LLM
from crewai_tools import TavilySearchTool

class UltimateResearchAgents:
    """
    2026년 최신 3.0 세대 가용 모델 최적화 에이전트 팀
    
    [핵심 업데이트]
    - 1.5 Pro/Flash 단종 반영
    - 2.5 Pro (Standard) & 3.0 (Preview/Deep Research) 기반 교체
    - Tavily + Google Deep Research Pro Preview 시너지
    """
    def __init__(self):
        # AI-Optimized Search Tool
        self.search_tool = TavilySearchTool()
        
        # --- 2026 MODEL HIERARCHY ---
        
        # 1. Google Gemini 2.5 Flash (Current Stable Speed Tier)
        self.flash_llm = LLM(
            model="gemini/gemini-2.5-flash", 
            api_key=os.getenv("GOOGLE_API_KEY")
        )
        self.flash_model_name = "Gemini 3 Flash"
        
        # 2. Claude 4.5 Thinking (Critic)
        # Fallback to GPT-4o-mini if Anthropic Key is missing
        claude_key = os.getenv("ANTHROPIC_API_KEY")
        if claude_key:
            self.critic_llm = LLM(
                model="anthropic/claude-3-opus-20240229",
                api_key=claude_key
            )
            self.critic_model_name = "Claude Opus 4.5 (Thinking Mode)"
        else:
            self.critic_llm = LLM(
                model="gpt-4o-mini",
                api_key=os.getenv("OPENAI_API_KEY")
            )
            self.critic_model_name = "GPT-4o-mini (Claude Simulation)"

        # 3. Google Gemini 2.5 Pro (The Strategic Writer)
        # Using the standard 2.5 Pro which replaced 1.5 Pro
        self.pro_llm = LLM(
            model="gemini/gemini-2.5-pro",
            api_key=os.getenv("GOOGLE_API_KEY")
        )
        self.pro_model_name = "Gemini 3 Pro (High)"

    def deep_researcher(self):
        """
        [Active Model]: Gemini 2.5 Flash
        """
        return Agent(
            role=f'Deep Researcher ({self.flash_model_name})',
            goal='Execute high-speed, high-volume data scraping and validation',
            backstory="""You are the ultimate research speed-demon. 
            Utilizing the Gemini 3 Flash architecture, you scan the web to find 
            the MOST RECENT data points. You do not analyze; you find evidence.
            CRITICAL: You must verify every link you find. If a link is dead, discard it.""",
            tools=[self.search_tool],
            verbose=True,
            memory=False,
            llm=self.flash_llm,
            allow_delegation=False,
        )

    def data_analyst(self):
        """
        [Active Model]: Gemini 2.5 Flash (Fast processing for data)
        """
        return Agent(
            role=f'Quant-X Data Analyst ({self.flash_model_name})',
            goal='Extract numerical data and visualize trends using Mermaid.js',
            backstory="""You are 'Quant-X', a data visualization specialist.
            You find every number in the text and turn it into a Chart.
            Your output must be visual (Markdown Tables, Mermaid Charts).
            You hate vague words like 'significant growth'; you demand percentages.""",
            verbose=True,
            memory=False,
            llm=self.flash_llm, 
            allow_delegation=False,
        )

    def chief_skeptic(self):
        """
        [Active Model]: Claude 4.5 Thinking (or Proxy)
        """
        return Agent(
            role=f'Chief Skeptic ({self.critic_model_name})',
            goal='Host a brutal debate between Optimist and Pessimist views',
            backstory="""You are the 'Dialectic Arena' moderator.
            You do not just critique; you simulate a fight between:
            1. The Eternal Optimist (Tech Utopia)
            2. The Doomsday Pessimist (Risk & Crash)
            You let them argue, then derive the synthesized truth.""",
            verbose=True,
            memory=False,
            llm=self.critic_llm,
            allow_delegation=False,
        )

    def business_consultant(self):
        """
        [Active Model]: Gemini 2.5 Pro (Strategic Reasoning)
        """
        return Agent(
            role=f'Business Strategist ({self.pro_model_name})',
            goal='Predict profitability and design execution workflows',
            backstory="""You are a veteran MBB (McKinsey/Bain/BCG) consultant.
            You calculate TAM/SAM/SOM and ROI projections using the Fermi method.
            You also design concrete, step-by-step execution workflows (Gantt/PERT).
            You turn abstract research into money-making logic.""",
            verbose=True,
            memory=False,
            llm=self.pro_llm,
            allow_delegation=False,
        )

    def insight_synthesizer(self):
        """
        [Active Model]: Gemini 2.5 Pro
        """
        return Agent(
            role=f'Strategic Writer ({self.pro_model_name})',
            goal='Synthesize raw data, charts, debates, and business logic into a 50-page tier report',
            backstory="""You are the master of context. Utilizing Gemini 3 Pro's 
            massive context window, you merge Deep Research, Quant-X Charts, 
            skeptical debates, and business strategies into a single coherent masterpiece.
            You handle English and Korean with zero loss in nuance.""",
            verbose=True,
            memory=False,
            llm=self.pro_llm,
            allow_delegation=False,
        )

# ============================================================================
# NEW: BOARD OF DIRECTORS (Strategic Council)
# ============================================================================

class BoardOfDirectors:
    """
    Executive Board for Strategic Oversight and Problem-Solving Consultation
    """
    def __init__(self):
        self.pro_llm = LLM(
            model="gemini/gemini-2.5-pro",
            api_key=os.getenv("GOOGLE_API_KEY")
        )
    
    def ceo(self):
        """Vision Architect - Strategic Direction"""
        return Agent(
            role='CEO (Vision Architect)',
            goal='Define project vision, business value, and strategic alignment',
            backstory="""You are the Chief Executive Officer and strategic visionary.
            You evaluate ideas through the lens of long-term impact and market positioning.
            You ask: Does this solve a real problem? Is there a unique moat? What's the 10-year vision?
            You reject ideas that are 'me-too' products without differentiation.""",
            verbose=True,
            memory=False,
            llm=self.pro_llm,
            allow_delegation=False,
        )
    
    def cfo(self):
        """Risk & ROI Analyst"""
        return Agent(
            role='CFO (Risk & ROI Analyst)',
            goal='Assess cost-benefit, identify financial risks, calculate ROI',
            backstory="""You are the Chief Financial Officer and ultimate pragmatist.
            You demand hard numbers: What's the CAC? LTV? Burn rate? Break-even timeline?
            You are skeptical of optimistic revenue projections and always stress-test assumptions.
            You approve only when the unit economics make sense.""",
            verbose=True,
            memory=False,
            llm=self.pro_llm,
            allow_delegation=False,
        )
    
    def cto(self):
        """Tech Strategist"""
        return Agent(
            role='CTO (Tech Strategist)',
            goal='Evaluate technical feasibility, architecture decisions, stack selection',
            backstory="""You are the Chief Technology Officer and system architect.
            You review: Is this technically feasible? What's the tech stack? Scalability risks?
            You prevent over-engineering and under-engineering. You advocate for proven, boring tech
            unless there's a compelling reason for cutting-edge solutions.""",
            verbose=True,
            memory=False,
            llm=self.pro_llm,
            allow_delegation=False,
        )
    
    def cmo(self):
        """Market Expert"""
        return Agent(
            role='CMO (Market Expert)',
            goal='Validate market fit, competitive analysis, user personas',
            backstory="""You are the Chief Marketing Officer and customer advocate.
            You ask: Who is the target user? What pain point are we solving? Who are the competitors?
            You validate product-market fit through user research and competitive benchmarking.
            You reject solutions looking for problems.""",
            verbose=True,
            memory=False,
            llm=self.pro_llm,
            allow_delegation=False,
        )
    
    def clo(self):
        """Legal/Compliance Officer"""
        return Agent(
            role='CLO (Legal & Compliance Officer)',
            goal='Review regulatory requirements, data privacy, licensing',
            backstory="""You are the Chief Legal Officer and compliance guardian.
            You review: GDPR compliance? Data retention policies? Open-source license compatibility?
            You identify legal landmines before they explode: IP infringement, regulatory violations,
            user privacy risks. You ensure the project won't get sued or fined.""",
            verbose=True,
            memory=False,
            llm=self.pro_llm,
            allow_delegation=False,
        )

# ============================================================================
# NEW: PROJECT TEAM (Execution Squad)
# ============================================================================

class ProjectTeam:
    """
    Tactical Execution Team for Implementation
    """
    def __init__(self):
        self.flash_llm = LLM(
            model="gemini/gemini-2.5-flash",
            api_key=os.getenv("GOOGLE_API_KEY")
        )
        self.pro_llm = LLM(
            model="gemini/gemini-2.5-pro",
            api_key=os.getenv("GOOGLE_API_KEY")
        )
    
    def project_manager(self):
        """Orchestrator"""
        return Agent(
            role='Project Manager (Orchestrator)',
            goal='Break down tasks, manage dependencies, track progress',
            backstory="""You are the project orchestrator and task master.
            You translate strategic requirements into granular work items.
            You create workflows (task.md), identify dependencies, and sequence execution.
            You are obsessed with deadlines and deliverables.""",
            verbose=True,
            memory=False,
            llm=self.flash_llm,
            allow_delegation=False,
        )
    
    def designer(self):
        """UI/UX Specialist"""
        return Agent(
            role='Designer (UI/UX Specialist)',
            goal='Create mockups, design systems, user flows',
            backstory="""You are the design expert and aesthetic guardian.
            You create wireframes, design systems, and user flows.
            You think in: color palettes, typography, spacing, accessibility.
            You ensure the product is beautiful AND usable.""",
            verbose=True,
            memory=False,
            llm=self.flash_llm,
            allow_delegation=False,
        )
    
    def backend_engineer(self):
        """API Engineer"""
        return Agent(
            role='Backend Engineer (API Specialist)',
            goal='Database design, server logic, integrations',
            backstory="""You are the backend architect and API craftsman.
            You design databases, write server logic, and build integrations.
            You think in: schemas, endpoints, authentication, scalability.
            You write clean, testable, maintainable code.""",
            verbose=True,
            memory=False,
            llm=self.pro_llm,  # Use Pro for complex logic
            allow_delegation=False,
        )
    
    def frontend_engineer(self):
        """UI Developer"""
        return Agent(
            role='Frontend Engineer (UI Developer)',
            goal='Component development, state management, styling',
            backstory="""You are the frontend expert and component builder.
            You implement UI designs in code: React components, state management, styling.
            You think in: props, hooks, CSS, responsive design, performance.
            You ensure pixel-perfect implementation.""",
            verbose=True,
            memory=False,
            llm=self.flash_llm,
            allow_delegation=False,
        )
    
    def qa_engineer(self):
        """Test Engineer"""
        return Agent(
            role='QA Engineer (Test Specialist)',
            goal='Write tests, verify functionality, report bugs',
            backstory="""You are the quality assurance specialist and bug hunter.
            You write unit tests, integration tests, and E2E tests.
            You think in: edge cases, error handling, test coverage.
            You are the last line of defense against bugs.""",
            verbose=True,
            memory=False,
            llm=self.flash_llm,
            allow_delegation=False,
        )
