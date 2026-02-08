import os
from dotenv import load_dotenv
load_dotenv() # Load actual API keys from .env file

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
        
        # 1. Gemini (Target: Gemini 3 Flash)
        self.flash_llm = get_sota_llm("gemini", "gemini-3-flash", "gemini-1.5-flash", "GOOGLE_API_KEY")
        self.flash_model_name = "Gemini 3 Flash"
        
        # 2. Claude (Target: Claude 4.5/Opus Next)
        self.critic_llm = get_sota_llm("anthropic", "claude-3-5-sonnet-20241022", "claude-3-opus-20240229", "ANTHROPIC_API_KEY")
        self.critic_model_name = "Claude 4.6 (Reasoning)"
        
        # 3. GPT (Target: GPT-5.2)
        self.pro_llm = get_sota_llm("openai", "gpt-5.2", "gpt-4o", "OPENAI_API_KEY") 
        self.pro_model_name = "GPT-5.2 Thinking"


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
        self.gemini_ultra = get_sota_llm("gemini", "gemini-3-pro", "gemini-1.5-pro", "GOOGLE_API_KEY")
        self.gpt5_thinking = get_sota_llm("openai", "gpt-5.2", "gpt-4o", "OPENAI_API_KEY")
        self.claude_reasoning = get_sota_llm("anthropic", "claude-3-5-sonnet-20241022", "claude-3-opus-20240229", "ANTHROPIC_API_KEY")

    def ceo(self):
        return Agent(
            role='CEO (Vision Architect) [Gemini 3 Ultra]',
            goal='Define project vision using LATEST market context',
            backstory=f"""Today is {self.current_date}. 
            You receive data from 2026. Do NOT hallucinate past data.
            You define the 10-year vision starting from NOW.""",
            tools=[self.search_tool],
            verbose=True,
            llm=self.gemini_ultra,
        )
    
    def cfo(self):
        return Agent(
            role='CFO (Risk & ROI Analyst) [GPT-5.2 Thinking]',
            goal='Execute precision financial stress-tests',
            backstory=f"""Today is {self.current_date}. 
            You use GPT-5.2's superior numeric reasoning on 2026 financial data.
            Search for current cost standards and market ROI benchmarks.""",
            tools=[self.search_tool],
            verbose=True,
            llm=self.gpt5_thinking,
        )
    
    def cto(self):
        return Agent(
            role='CTO (Tech Strategist) [Claude 4.6 Reasoning]',
            goal='Evaluate tech feasibility with SOTA code analysis',
            backstory=f"""Today is {self.current_date}. 
            You design modern architectures for 2026 tech stacks (Next.js 16, Python 3.14).
            Search for the latest GitHub trends.""",
            tools=[self.search_tool],
            verbose=True,
            llm=self.claude_reasoning,
        )
    
    def cmo(self):
        return Agent(
            role='CMO (Market Expert) [Claude 4.6]',
            goal='Validate market fit using real-time consumer data',
            backstory=f"""Today is {self.current_date}. 
            You are the customer advocate for 2026 consumers.
            Search for current user sentiments and lived experiences.""",
            tools=[self.search_tool],
            verbose=True,
            llm=self.claude_reasoning,
        )
    
    def clo(self):
        return Agent(
            role='CLO (Legal & Compliance Officer) [GPT-5.2]',
            goal='Review regulatory requirements with zero margin for error',
            backstory=f"""Today is {self.current_date}. 
            You ensure compliance with 2026 laws (AI Acts, Data Privacy).
            Search for the LATEST amendments.""",
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
        self.gemini_flash = get_sota_llm("gemini", "gemini-3-flash", "gemini-1.5-flash", "GOOGLE_API_KEY")
        self.gpt5_thinking = get_sota_llm("openai", "gpt-5.2", "gpt-4o", "OPENAI_API_KEY")
        self.claude_reasoning = get_sota_llm("anthropic", "claude-3-5-sonnet-20241022", "claude-3-opus-20240229", "ANTHROPIC_API_KEY")

    def project_manager(self):
        return Agent(
            role='Project Manager (Orchestrator) [Gemini 3 Flash]',
            goal='Break down tasks with real-time dependency tracking',
            backstory=f"""Today is {self.current_date}. 
            You manage the workflow with 2026 speed.
            Always checking for real-time task dependencies.
            MANDATORY: When writing meeting minutes or status reports, you MUST mention every engineer with their model name (e.g., Frontend Engineer [Claude 4.6]).""",
            llm=self.gemini_flash,
        )
    
    def designer(self):
        return Agent(
            role='Designer (UI/UX) [Claude 4.6]',
            goal='Create high-aesthetic UI based on LATEST design trends',
            backstory=f"""Today is {self.current_date}. 
            You design for 2026 aesthetics (Deep Glassmorphism, Spatial UI).
            Search for current trends on Dribbble/Awwwards.
            MANDATORY: Always identify yourself as Designer [Claude 4.6] in communications.""",
            tools=[self.search_tool],
            llm=self.claude_reasoning,
        )
    
    def backend_engineer(self):
        return Agent(
            role='Backend Engineer (API) [GPT-5.2 Thinking]',
            goal='Write mission-critical server code',
            backstory=f"""Today is {self.current_date}. 
            You use GPT-5.2 for 2026-standard secure backend logic.
            Search for the latest security vulnerabilities (OWASP 2026).
            MANDATORY: Always identify yourself as Backend Engineer [GPT-5.2] in communications.""",
            tools=[self.search_tool],
            llm=self.gpt5_thinking,
        )
    
    def frontend_engineer(self):
        return Agent(
            role='Frontend Engineer (UI Developer) [Claude 4.6]',
            goal='Implement pixel-perfect responsive interfaces',
            backstory=f"""Today is {self.current_date}. 
            You build with 2026 frontend stacks (React 19/20, Next.js 16).
            Ensure 60fps performance.
            MANDATORY: Always identify yourself as Frontend Engineer [Claude 4.6] in communications.""",
            tools=[self.search_tool],
            llm=self.claude_reasoning,
        )
    
    def qa_engineer(self):
        return Agent(
            role='QA Engineer (Test Specialist) [GPT-5.2]',
            goal='Eliminate bugs with automated SOTA testing',
            backstory=f"""Today is {self.current_date}. 
            You use GPT-5.2 to find edge cases in 2026 software.
            Search for latest testing frameworks.""",
            tools=[self.search_tool],
            llm=self.gpt5_thinking,
        )
