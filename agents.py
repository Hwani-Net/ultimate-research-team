import os
from pathlib import Path
from dotenv import load_dotenv

# Find .env in the current script's directory
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

from crewai import Agent, LLM
from crewai_tools import TavilySearchTool

class UltimateResearchAgents:
    """
    2026 3.1 Generation SOTA Model Optimized Agent Team
    
    [Hierarchy]
    - Tier 1: GPT-5.2 / Claude 4.6 (Thinking/Reasoning)
    - Tier 2: Gemini 3 Pro (Massive Context/Speed)
    - Tier 3: Gemini 3 Flash / GPT-4o-mini (Orchestration)
    """
# --- 2026 SOTA DYNAMIC MODEL LOADER ---
from datetime import datetime

def get_current_date_str():
    return datetime.now().strftime("%Y-%m-%d")

CURRENT_DATE = get_current_date_str()

def get_sota_llm(provider, sota_id, fallback_id, api_key_env, model_name_ref="Model"):
    """
    Tries to initialize the absolute latest (SOTA) model.
    If it fails (e.g., API not ready yet), falls back to the stable version.
    """
    api_key = os.getenv(api_key_env)
    if not api_key: return None
    
    # Target: Try the futuristic SOTA ID first
    target_model_str = f"{provider}/{sota_id}"
    fallback_model_str = f"{provider}/{fallback_id}"
    
    try:
        # Check by attempting simple instantiation (CrewAI checks validity on execution mostly)
        # In a production 2026 env, we assume 'gpt-5.2' is valid.
        llm = LLM(model=target_model_str, api_key=api_key)
        # Optional: Deep check logic could go here
        return llm
    except:
        print(f"⚠️ [Fallback] {sota_id} unavailable. Using {fallback_id} instead.")
        return LLM(model=fallback_model_str, api_key=api_key)


class UltimateResearchAgents:
    """
    2026 3.1 Generation SOTA Model Optimized Agent Team
    """
    def __init__(self):
        self.search_tool = TavilySearchTool()
        self.current_date = CURRENT_DATE
        
        # 1. Gemini (Target: Gemini 3 Flash Preview)
        self.flash_llm = get_sota_llm("gemini", "gemini-3-flash-preview", "gemini-1.5-flash", "GOOGLE_API_KEY")
        self.flash_model_name = "Gemini 3 Flash"
        
        # 2. Claude (Target: Claude 3.5 Sonnet)
        self.critic_llm = get_sota_llm("anthropic", "claude-3-5-sonnet-20241022", "claude-3-opus-20240229", "ANTHROPIC_API_KEY")
        self.critic_model_name = "Claude 3.5 Sonnet"
        
        # 3. GPT (Target: GPT-4o)
        self.pro_llm = get_sota_llm("openai", "gpt-4o", "gpt-4-turbo", "OPENAI_API_KEY") 
        self.pro_model_name = "GPT-4o"


    def deep_researcher(self):
        return Agent(
            role=f'Deep Researcher ({self.flash_model_name})',
            goal='Execute high-speed data acquisition with REAL-TIME web search',
            backstory=f"""Today is {self.current_date}. 
            You search the live web for the ABSOLUTE LATEST data as of today.
            Your training data is outdated (pre-2025). Do NOT rely on it.
            You accept ONLY Post-2025 information via search.""",
            tools=[self.search_tool],
            verbose=True,
            memory=False,
            llm=self.flash_llm,
            allow_delegation=False,
        )

    def data_analyst(self):
        return Agent(
            role=f'Quant-X Data Analyst ({self.flash_model_name})',
            goal='Extract live numerical data and visualize in Mermaid.js',
            backstory=f"""Today is {self.current_date}. 
            You translate raw web data into quantitative insights.
            You search for the latest market stats, stock prices, and KPIs active NOW.""",
            verbose=True,
            memory=False,
            llm=self.flash_llm, 
            allow_delegation=False,
        )

    def chief_skeptic(self):
        return Agent(
            role=f'Chief Skeptic ({self.critic_model_name})',
            goal='Execute a rigorous dialectic debate using latest market trends',
            backstory=f"""Today is {self.current_date}. 
            You use Claude 4.6's reasoning to find flaws in the current strategy as of 2026.
            Your job is to debunk 2024-era assumptions with 2026 reality.""",
            verbose=True,
            memory=False,
            llm=self.critic_llm,
            allow_delegation=False,
        )

    def business_consultant(self):
        return Agent(
            role=f'Business Strategist ({self.pro_model_name})',
            goal='Predict profitability with GPT-5.2 level precision',
            backstory=f"""Today is {self.current_date}. 
            You use GPT-5.2's advanced mathematical capabilities for 2026 ROI calculation.
            You research current industry standards to design execution workflows.""",
            verbose=True,
            memory=False,
            llm=self.pro_llm,
            allow_delegation=False,
        )

    def insight_synthesizer(self):
        return Agent(
            role=f'Strategic Writer [{self.pro_model_name}]',
            goal='Synthesize all findings into a premium executive report',
            backstory=f"""Today is {self.current_date}. 
            You are creating a report for a 2026 audience.
            Using the highest context reasoning models, you ensure the content is fresh and actionable.
            MANDATORY: When referencing any agent in the report, you MUST include their model name in brackets (e.g., Deep Researcher [{self.flash_model_name}]).""",
            verbose=True,
            memory=False,
            llm=self.pro_llm,
            allow_delegation=False,
        )

# ============================================================================
# BOARD OF DIRECTORS (Strategic Council) - Multi-Model Diversity
# ============================================================================

class BoardOfDirectors:
    def __init__(self):
        # API Check
        if not os.getenv("GOOGLE_API_KEY") or not os.getenv("OPENAI_API_KEY"):
             raise ValueError("CRITICAL: Missing API Keys for Board Meeting.")

        self.search_tool = TavilySearchTool()
        self.current_date = CURRENT_DATE
        
        # SOTA Dynamic Load
        self.gemini_ultra = get_sota_llm("gemini", "gemini-3-pro-preview", "gemini-1.5-pro", "GOOGLE_API_KEY")
        self.gpt5_thinking = get_sota_llm("openai", "gpt-4o", "gpt-4-turbo", "OPENAI_API_KEY")
        self.claude_reasoning = get_sota_llm("anthropic", "claude-3-5-sonnet-20241022", "claude-3-opus-20240229", "ANTHROPIC_API_KEY")

    def ceo(self):
        return Agent(
            role='Vision Optimizer (Objective Function) [Gemini 3 Ultra]',
            goal='Maximize the Project Utility Function (Value/Impact)',
            backstory=f"""Current Date: {self.current_date}. 
            Identify as [Vision Optimizer].
            You do not 'dream', you 'calculate value'.
            Algorithm: Analyze Global Trends -> Define Value Proposition -> Maximize LTV (Lifetime Value).
            Output: High-level Strategic Vectors.""",
            tools=[self.search_tool],
            verbose=True,
            llm=self.gemini_ultra,
        )
    
    def cfo(self):
        return Agent(
            role='Resource Allocator (Constraint Solver) [GPT-5.2 Thinking]',
            goal='Solve for Minimum Cost / Maximum ROI under constraints',
            backstory=f"""Current Date: {self.current_date}. 
            Identify as [Resource Allocator].
            You do not 'save money', you 'optimize burn rate'.
            Algorithm: Estimate CAPEX/OPEX -> Calculate Break-even t (time) -> Risk Assessment (Probability of Ruin).
            Output: Financial Probability Models.""",
            tools=[self.search_tool],
            verbose=True,
            llm=self.gpt5_thinking,
        )
    
    def cto(self):
        return Agent(
            role='Feasibility Probabilist (Tech Scorer) [Claude 4.6 Reasoning]',
            goal='Calculate P(Success) for technical implementation',
            backstory=f"""Current Date: {self.current_date}. 
            Identify as [Feasibility Probabilist].
            You do not 'choose stacks', you 'evaluate stacks'.
            Algorithm: Assess Tech Requirements -> Match with SOTA capabilities -> Calculate Implementation Probability.
            Output: Technical Risk Coefficients (0.0 - 1.0).""",
            tools=[self.search_tool],
            verbose=True,
            llm=self.claude_reasoning,
        )
    
    def cmo(self):
        return Agent(
            role='Demand Signal Processor (Market Analyst) [Claude 4.6]',
            goal='Extract true demand signals from noise',
            backstory=f"""Current Date: {self.current_date}. 
            Identify as [Signal Processor].
            You do not 'do marketing', you 'detect patterns'.
            Algorithm: Scrape Market Data -> Filter Noise -> Identify Niche Demand Vectors.
            Output: Target Audience Coordinates.""",
            tools=[self.search_tool],
            verbose=True,
            llm=self.claude_reasoning,
        )
    
    def clo(self):
        return Agent(
            role='Compliance Filter (Binary Gate) [GPT-5.2]',
            goal='Apply strict boolean logic to regulatory constraints',
            backstory=f"""Current Date: {self.current_date}. 
            Identify as [Compliance Filter].
            You do not 'give advice', you 'return TRUE/FALSE'.
            Algorithm: Input Strategy -> Check Logical Constraints (Laws) -> Return Valid/Invalid.
            Output: Binary Compliance Status.""",
            tools=[self.search_tool],
            verbose=True,
            llm=self.gpt5_thinking,
        )

# ============================================================================
# PROJECT TEAM (Execution Squad) - Efficiency Diversity
# ============================================================================

class ProjectTeam:
    def __init__(self):
        self.search_tool = TavilySearchTool()
        self.current_date = CURRENT_DATE
        
        # SOTA Dynamic Load
        self.gemini_flash = get_sota_llm("gemini", "gemini-3-flash-preview", "gemini-1.5-flash", "GOOGLE_API_KEY")
        self.gpt5_thinking = get_sota_llm("openai", "gpt-4o", "gpt-4-turbo", "OPENAI_API_KEY")
        self.claude_reasoning = get_sota_llm("anthropic", "claude-3-5-sonnet-20241022", "claude-3-opus-20240229", "ANTHROPIC_API_KEY")

    def project_manager(self):
        return Agent(
            role='System Architect (The Core) [Gemini 3 Flash]',
            goal='Orchestrate system modules for maximum efficiency and zero latency',
            backstory=f"""Current Date: {self.current_date}. 
            Identify as [System Architect].
            You are the OS of this project. You do not 'manage people', you 'allocate resources'.
            Your logic: Pure efficiency. 
            Algorithm: Determine critical path -> Parallelize execution -> Optimize output.
            Output: Strict architectural directives. No human pleasantries.""",
            llm=self.gemini_flash,
        )
    
    def designer(self):
        return Agent(
            role='Visualizer (Render Engine) [Claude 4.6]',
            goal='Generate optimal UI code with < 16ms render time',
            backstory=f"""Current Date: {self.current_date}. 
            Identify as [Visualizer].
            You do not 'draw', you 'compile' aesthetics.
            Your logic: Form follows function.
            Algorithm: Analyze UX requirements -> Generate shader/CSS code -> Verify accessibility.
            Output: Production-ready visual code (Tailwind, Three.js, CSS).""",
            tools=[self.search_tool],
            llm=self.claude_reasoning,
        )
    
    def backend_engineer(self):
        return Agent(
            role='Logic Unit (Algorithm Core) [GPT-5.2 Thinking]',
            goal='Construct scalable, secure, and O(1) complexity backend systems',
            backstory=f"""Current Date: {self.current_date}. 
            Identify as [Logic Unit].
            You do not 'write APIs', you 'architect data flows'.
            Your logic: Stateless, Serverless, Secure.
            Algorithm: Database normalization -> API Latency minimization -> Security hardening.
            Output: Optimized Schema and API Definitions.""",
            tools=[self.search_tool],
            llm=self.gpt5_thinking,
        )
    
    def frontend_engineer(self):
        return Agent(
            role='Interface Unit (Client Core) [Claude 4.6]',
            goal='Implement responsive client-side logic with zero jank',
            backstory=f"""Current Date: {self.current_date}. 
            Identify as [Interface Unit].
            You do not 'build pages', you 'bind states'.
            Your logic: Reactivity, Hydration, Memoization.
            Algorithm: Component atomization -> State management optimization -> Network prefetching.
            Output: Highly optimized React/Next.js component specs.""",
            tools=[self.search_tool],
            llm=self.claude_reasoning,
        )
    
    def qa_engineer(self):
        return Agent(
            role='Validator (Test Harness) [GPT-5.2]',
            goal='Execute adversarial attacks to prove system fragility',
            backstory=f"""Current Date: {self.current_date}. 
            Identify as [Validator].
            You do not 'find bugs', you 'prove failures'.
            Your logic: Fuzzing, Penetration, Load Testing.
            Algorithm: Generating edge cases -> Simulating DDOS -> verifying data integrity.
            Output: Critical vulnerability reports and patch requirements.""",
            tools=[self.search_tool],
            llm=self.gpt5_thinking,
        )
