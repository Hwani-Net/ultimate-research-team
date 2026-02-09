import streamlit as st
import os

# --- Streamlit Cloud / Multi-threaded Compatibility Patch ---
import os
import signal
import threading

# 1. Disable Telemetry
os.environ["CREWAI_DISABLE_TELEMETRY"] = "1"
os.environ["LITELLM_MODE"] = "PRODUCTION"

# 2. Monkey-patch signal to ignore non-main thread errors
_original_signal = signal.signal

def _safe_signal_handler(sig, handler):
    try:
        if threading.current_thread() is not threading.main_thread():
            return None
        return _original_signal(sig, handler)
    except ValueError:
        # "signal only works in main thread" error -> Ignore it
        return None

signal.signal = _safe_signal_handler

import sys
import subprocess

# --- EMERGENCY DEPENDENCY PATCH ---
def ensure_dependencies():
    try:
        import tavily
    except ImportError:
        print("🔧 [PATCH] Installing missing tavily-python dependency...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "tavily-python"])
            print("✅ [PATCH] tavily-python installed.")
        except Exception as e:
            print(f"❌ [PATCH] Failed to install tavily-python: {e}")

ensure_dependencies()
# ----------------------------------

import contextlib
import io
import re
from crewai import Crew, Process

# Set Timezone to KST
os.environ["TZ"] = "Asia/Seoul"
if sys.platform != "win32":
    try:
        import time
        time.tzset()
    except Exception:
        pass
from agents import UltimateResearchAgents, BoardOfDirectors, ProjectTeam
from tasks import UltimateResearchTasks, BoardTasks, ProjectTeamTasks
from dotenv import load_dotenv
import datetime
try:
    import pytz
    KST = pytz.timezone('Asia/Seoul')
except ImportError:
    KST = datetime.timezone(datetime.timedelta(hours=9))

# Page Config
st.set_page_config(page_title="Ultimate Research Team (v11.5)", page_icon="🧠", layout="wide")

# Custom CSS for Premium Look & Real-time Logs
if 'theme' not in st.session_state:
    st.session_state.theme = 'Dark'

with st.sidebar:
    st.radio("🌗 Theme Mode", ["Dark", "Light"], horizontal=True, label_visibility="collapsed", key="theme")

# Define Theme Palettes
if st.session_state.theme == 'Dark':
    primary_gradient = "linear-gradient(135deg, #14b8a6 0%, #3b82f6 50%, #6366f1 100%)" 
    bg_color = "#0a0f1e" # Rich Executive Navy
    bg_image = """radial-gradient(at 0% 0%, rgba(20, 184, 166, 0.1) 0, transparent 50%), 
                  radial-gradient(at 100% 0%, rgba(99, 102, 241, 0.1) 0, transparent 50%)"""
    text_color = "#e2e8f0" # High-contrast off-white
    glass_bg = "rgba(15, 23, 42, 0.75)"
    glass_border = "rgba(255, 255, 255, 0.05)"
    sidebar_css = """
        background: linear-gradient(180deg, #070b14 0%, #0a0f1e 100%) !important;
    """
    console_bg = "rgba(2, 6, 23, 0.95)"
    console_text = "#5eead4"
    report_bg = "rgba(255, 255, 255, 0.02)"
    
else:  # Light Mode (Clean Executive)
    primary_gradient = "linear-gradient(135deg, #0d9488 0%, #2563eb 50%, #4f46e5 100%)" 
    bg_color = "#f8fafc" 
    bg_image = """radial-gradient(at 0% 0%, rgba(20, 184, 166, 0.05) 0, transparent 50%), 
                  radial-gradient(at 100% 0%, rgba(79, 70, 229, 0.05) 0, transparent 50%)"""
    text_color = "#0f172a" 
    glass_bg = "rgba(255, 255, 255, 0.85)"
    glass_border = "rgba(148, 163, 184, 0.2)"
    sidebar_css = """
        background-color: #ffffff !important;
    """
    console_bg = "#0f172a" 
    console_text = "#f1f5f9"
    report_bg = "rgba(241, 245, 249, 0.95)"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

:root {{
    --primary-gradient: {primary_gradient};
    --glass-bg: {glass_bg};
    --glass-border: {glass_border};
    --accent-glow: 0 0 25px rgba(20, 184, 166, 0.25);
    --text-color: {text_color};
    --console-bg: {console_bg};
    --console-text: {console_text};
    --report-bg: {report_bg};
}}

/* Global Text Reset */
html, body, [class*="css"] {{
    font-family: 'Inter', -apple-system, sans-serif;
    color: var(--text-color) !important;
    letter-spacing: -0.01em;
}}

/* Main Background */
.stApp {{
    background-color: {bg_color};
    background-image: {bg_image};
    background-attachment: fixed;
    animation: page-in 0.6s ease-out;
}}

.block-container {{
    padding-top: 2.2rem !important;
    padding-bottom: 3rem !important;
}}

/* Column Layout Smoothing */
[data-testid="stHorizontalBlock"] {{
    gap: 14px;
    align-items: stretch;
}}

[data-testid="stVerticalBlockBorderWrapper"] {{
    height: 100%;
}}

.panel-body {{
    min-height: 560px;
    padding: 0;
}}

.panel-body .console-box {{
    height: 560px;
    margin: 0;
    border-radius: 16px;
}}

.panel-live {{
    margin-top: -10px;
}}

.panel-live .console-box {{
    height: 570px;
}}

.panel-compact {{
    min-height: 360px;
}}

.panel-compact .stTextArea textarea {{
    min-height: 140px;
}}

::selection {{
    background: rgba(249, 115, 22, 0.35);
    color: #0b0f14;
}}

/* Sidebar - Force Override */
[data-testid="stSidebar"] {{
    {sidebar_css}
    border-right: 1px solid var(--glass-border);
    box-shadow: 12px 0 40px rgba(0, 0, 0, 0.08);
}}

[data-testid="stSidebarUserContent"] {{
    padding-bottom: 100px !important;
}}

[data-testid="stSidebar"] * {{
    color: var(--text-color) !important;
}}

/* Markdown Text Specifics */
.stMarkdown p, .stMarkdown li, .stMarkdown span {{
    color: var(--text-color) !important;
    font-size: 1.05em;
    line-height: 1.6;
}}

h1, h2, h3, h4, h5, h6 {{
    font-family: 'Fraunces', serif;
    color: var(--text-color) !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
}}

/* Glass Cards */
div[data-testid="stVerticalBlockBorderWrapper"] {{
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--glass-border) !important;
    border-radius: 22px;
    padding: 24px 26px;
    margin-bottom: 24px;
    box-shadow: 0 12px 32px rgba(10, 20, 30, 0.16);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}

div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
    transform: translateY(-4px);
    box-shadow: 0 16px 36px rgba(10, 20, 30, 0.22);
}}

/* Buttons */
.stButton > button {{
    width: 100%;
    border-radius: 12px;
    height: 3.5em;
    background: var(--primary-gradient);
    color: white !important;
    font-weight: 700;
    border: none;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.18);
}}

.stButton > button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 16px 30px rgba(15, 23, 42, 0.22);
    color: white !important;
}}

/* Inputs & Selectboxes */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {{
    background-color: var(--glass-bg) !important;
    color: var(--text-color) !important;
    caret-color: var(--text-color) !important; /* Fix cursor visibility */
    border: 1px solid var(--glass-border) !important;
    border-radius: 12px;
}}

.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {{
    color: var(--text-color) !important;
    opacity: 0.5;
}}

/* Code Blocks & Terminal */
[data-testid="stCode"] {{
    background-color: var(--console-bg) !important;
    border-radius: 12px;
    border: 1px solid var(--glass-border);
    padding: 10px;
}}

[data-testid="stCode"] pre {{
    background-color: transparent !important;
    border: none !important;
}}

[data-testid="stCode"] code {{
    background-color: transparent !important;
    font-family: 'Space Mono', monospace !important;
    color: var(--console-text) !important; /* Force text color */
}}

/* Override potential syntax highlighting spans that might be invisible */
[data-testid="stCode"] span {{
    color: inherit;
}}

/* Console Box */
.console-box {{
    background-color: {console_bg};
    color: {console_text} !important;
    padding: 18px 18px;
    border-radius: 16px;
    font-family: 'Space Mono', monospace;
    height: 560px;
    overflow-y: auto;
    font-size: 0.85em;
    border: 1px solid rgba(20, 184, 166, 0.2);
}}

/* Report Card */
.report-card {{
    background: {report_bg};
    padding: 30px;
    border-radius: 20px;
    border: 1px solid var(--glass-border);
    color: var(--text-color) !important;
}}

/* Expander Styling */
[data-testid="stExpander"] {{
    border: none !important;
    box-shadow: none !important;
}}

[data-testid="stExpander"] details {{
    border-color: var(--glass-border) !important;
    background-color: var(--glass-bg) !important;
    border-radius: 12px;
    color: var(--text-color) !important;
}}

[data-testid="stExpander"] summary {{
    background-color: transparent !important;
    color: var(--text-color) !important;
    font-weight: 600 !important;
}}

[data-testid="stExpander"] summary:hover {{
    color: var(--text-color) !important;
    opacity: 0.8;
}}

[data-testid="stExpander"] summary p, 
[data-testid="stExpander"] summary span,
[data-testid="stExpander"] summary svg {{
    color: var(--text-color) !important;
    fill: var(--text-color) !important;
}}

/* Links */
a {{
    color: #0ea5a4 !important;
    text-decoration: none;
    font-weight: 600;
}}

/* Model Guide Badge */
.model-badge {{
    display: inline-block;
    padding: 6px 14px;
    border-radius: 10px;
    font-size: 0.75em;
    font-weight: 800;
    margin-right: 8px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    background: rgba(30, 41, 59, 0.1);
    border: 1px solid var(--glass-border);
    backdrop-filter: blur(5px);
}}
.badge-pro {{ color: #fbbf24; border-color: rgba(251, 191, 36, 0.3); background: rgba(251, 191, 36, 0.1); }}
.badge-flash {{ color: #34d399; border-color: rgba(52, 211, 153, 0.3); background: rgba(52, 211, 153, 0.1); }}
.badge-opus {{ color: #f87171; border-color: rgba(248, 113, 113, 0.3); background: rgba(248, 113, 113, 0.1); }}

.status-banner {{
    background: linear-gradient(90deg, rgba(20, 184, 166, 0.2), rgba(249, 115, 22, 0.2));
    border: 1px solid var(--glass-border);
    padding: 10px 20px;
    border-radius: 12px;
    text-align: center;
    font-weight: 600;
    font-size: 0.9em;
    margin-bottom: 30px;
    animation: pulse-glow 3s infinite;
    color: var(--text-color);
}}

/* Input Fields */
.stTextArea textarea {{
    background-color: var(--glass-bg) !important;
    color: var(--text-color) !important;
    border: 1px solid var(--glass-border) !important;
}}

/* Modal Dialog Customization for Dark Mode */
div[data-testid="stDialog"] {{
    background-color: #1e1e2f !important; /* Dark background */
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}}

div[data-testid="stDialog"] p, 
div[data-testid="stDialog"] h1,
div[data-testid="stDialog"] h2,
div[data-testid="stDialog"] h3 {{
    color: #ffffff !important;
}}

/* Modal TextArea specific override */
div[data-testid="stDialog"] textarea {{
    background-color: rgba(0, 0, 0, 0.3) !important;
    color: #e0e0e0 !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    font-size: 1.05em !important;
    line-height: 1.5 !important;
}}

div[data-testid="stDialog"] button[kind="secondary"] {{
    background-color: rgba(255, 255, 255, 0.1) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
}}

div[data-testid="stDialog"] button[kind="secondary"]:hover {{
    background-color: rgba(255, 255, 255, 0.2) !important;
    border: 1px solid rgba(255, 255, 255, 0.5) !important;
}}

/* Force Widget Labels High Visibility */
[data-testid="stWidgetLabel"], 
[data-testid="stWidgetLabel"] p,
label[data-baseweb="checkbox"] span,
label[data-baseweb="radio"] div {{
    color: var(--text-color) !important;
    font-weight: 600 !important;
    opacity: 1 !important;
}}

/* File Uploader Customization */
[data-testid="stFileUploader"] {{
    background-color: var(--glass-bg) !important;
    border-radius: 16px;
    padding: 10px;
    border: 1px dashed var(--glass-border);
}}

[data-testid="stFileUploaderDropzone"] {{
    background-color: rgba(255, 255, 255, 0.03) !important;
    border: none !important;
}}

/* File Uploader Text & Icons */
[data-testid="stFileUploaderDropzone"] div div span,
[data-testid="stFileUploaderDropzone"] div div small {{
    color: var(--text-color) !important;
    opacity: 0.9 !important;
}}

/* Uploaded File List */
[data-testid="stUploadedFile"] {{
    background-color: rgba(255, 255, 255, 0.05) !important;
    border-radius: 10px;
    margin-top: 5px;
    padding: 8px;
}}

[data-testid="stUploadedFile"] span,
[data-testid="stUploadedFile"] svg {{
    color: var(--text-color) !important;
}}

/* File Uploader Error Message visibility */
[data-testid="stErrorMessage"] {{
    background-color: rgba(255, 75, 75, 0.1) !important;
    border: 1px solid rgba(255, 75, 75, 0.3) !important;
    color: #ff4b4b !important;
    border-radius: 10px;
}}

[data-testid="stErrorMessage"] p {{
    color: #ff4b4b !important;
    font-weight: 600;
}}

.stSelectbox div[data-baseweb="select"] > div {{
    background-color: var(--glass-bg) !important;
    color: var(--text-color) !important;
    border: 1px solid var(--glass-border) !important;
}}

/* Custom Scrollbar */
::-webkit-scrollbar {{ width: 8px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{
    background: rgba(20, 184, 166, 0.35); 
    border-radius: 10px; 
}}
::-webkit-scrollbar-thumb:hover {{ background: rgba(20, 184, 166, 0.6); }}

@keyframes page-in {{
    from {{ opacity: 0; transform: translateY(12px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

@keyframes pulse-glow {{
    0% {{ box-shadow: 0 0 0 rgba(20, 184, 166, 0.0); }}
    50% {{ box-shadow: 0 0 18px rgba(20, 184, 166, 0.25); }}
    100% {{ box-shadow: 0 0 0 rgba(20, 184, 166, 0.0); }}
}}
</style>
""", unsafe_allow_html=True)

load_dotenv()

# Streamlit-compatible stdout capturing
class StreamlitCallbackHandler:
    def __init__(self, container):
        self.container = container
        self.text = ""

    def write(self, data):
        # Remove ANSI escape sequences (colors) from terminal output
        clean_text = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', data)
        self.text += clean_text
        self.container.markdown(f'<div class="console-box">{self.text}</div>', unsafe_allow_html=True)
    
    def flush(self):
        pass

def run_research(topic, log_container, image_data=None, research_mode="Deep Strategy (5-Agent)"):
    # Setup stdout redirect
    handler = StreamlitCallbackHandler(log_container)
    
    with contextlib.redirect_stdout(handler):
        print(f"🎯 [MISSION STARTED] Processing User Command: \"{topic}\"")
        print("--------------------------------------------------")
        
        # 1. Instantiate Agents
        agents = UltimateResearchAgents()
        
        # Common Agents
        researcher = agents.deep_researcher()
        writer = agents.insight_synthesizer()
        
        # 2. Instantiate Tasks
        tasks = UltimateResearchTasks()
        
        if research_mode == "Speed Briefing (3-Agent)":
            # 3-Agent Flow: Research -> Critic -> Writer
            critic = agents.chief_skeptic() # Re-using skeptic as critic
            
            t1 = tasks.initial_research_task(researcher, topic, image_data)
            # Utilizing a simplified critique task (need to ensure this exists or use debate task in a simple way)
            # For compatibility, we will use the debate task but purely for critique if we want, 
            # OR we can add a specific simple critique task back to tasks.py if needed. 
            # However, looking at the previous edit, I overwrote tasks.py. 
            # So I will use the 'debate_task' but instruct the agent to keep it brief, 
            # OR I will just use the research and direct writing for maximum speed?
            # Let's stick to the 3-agent structure: Research -> Debate(Critic) -> Write.
            
            t2 = tasks.debate_task(critic) # Using Skeptic for critique
            t3 = tasks.final_report_task(writer, topic)
            
            crew = Crew(
                agents=[researcher, critic, writer],
                tasks=[t1, t2, t3],
                verbose=True,
                process=Process.sequential,
                memory=False
            )
            
        else:
            # 5-Agent Flow: Research -> Data -> Debate -> Biz -> Writer
            analyst = agents.data_analyst()
            skeptic = agents.chief_skeptic()
            strategist = agents.business_consultant()
            
            t1 = tasks.initial_research_task(researcher, topic, image_data)
            t2 = tasks.data_visualization_task(analyst)
            t3 = tasks.debate_task(skeptic)
            t4 = tasks.business_logic_task(strategist)
            t5 = tasks.final_report_task(writer, topic)

            crew = Crew(
                agents=[researcher, analyst, skeptic, strategist, writer],
                tasks=[t1, t2, t3, t4, t5],
                verbose=True,
                process=Process.sequential,
                memory=False 
            )

        try:
            print("\n🚀 [EXECUTION] Kicking off CrewAI...")
            result = crew.kickoff()
            print("\n✅ [MISSION COMPLETE] Research Finished.")
            
            # 2026 CrewAI Update: Handle CrewOutput object
            if hasattr(result, 'raw'):
                return result.raw
            return str(result)
            
        except Exception as e:
            import traceback
            error_msg = f"❌ [CRITICAL ERROR] Research Failed: {str(e)}\n\n{traceback.format_exc()}"
            print(error_msg)
            return error_msg

def run_board_and_project_team(project_idea, log_container):
    """
    Dual-Layer Governance System: Board (Strategy) -> Project Team (Execution)
    """
    handler = StreamlitCallbackHandler(log_container)
    
    with contextlib.redirect_stdout(handler):
        print(f"🏛️ [BOARD GOVERNANCE] Initiating Project Screening...")
        print("=" * 70)
        
        # === PHASE 0: KILL SWITCH (PRE-BOARD SCREENING) ===
        print("\n🛡️ PHASE 0: KILL SWITCH - PRE-BOARD SCREENING")
        print("-" * 70)
        print("⚠️ Checking for FATAL FLAWS (trademark conflicts, extreme red ocean)...")
        
        board = BoardOfDirectors()
        from agents import UltimateResearchAgents
        research_team = UltimateResearchAgents()
        board_tasks = BoardTasks()
        
        # Get CLO and Deep Researcher for kill switch
        clo = board.clo()
        researcher = research_team.deep_researcher()
        
        # Run Kill Switch
        kill_switch_task = board_tasks.kill_switch_task(clo, researcher, project_idea)
        
        try:
            kill_switch_crew = Crew(
                agents=[clo, researcher],
                tasks=[kill_switch_task],
                verbose=True,
                process=Process.sequential,
                memory=False
            )
            
            print("\n🔍 Running Kill Switch Protocol...")
            kill_result = kill_switch_crew.kickoff()
            
            # Parse structured output
            if hasattr(kill_result, 'pydantic'):
                kill_data = kill_result.pydantic
            elif hasattr(kill_result, 'json_dict'):
                from models import KillSwitchResult
                kill_data = KillSwitchResult(**kill_result.json_dict)
            else:
                # Fallback: try to parse as dict
                import json
                from models import KillSwitchResult
                try:
                    kill_dict = json.loads(str(kill_result))
                    kill_data = KillSwitchResult(**kill_dict)
                except:
                    # Last resort: string check
                    kill_decision = str(kill_result)
                    if "KILL" in kill_decision.upper():
                        print("\n❌ [PROJECT TERMINATED BY KILL SWITCH]")
                        return f"## 🛑 Project Terminated\n\n{kill_decision}"
                    else:
                        print("\n✅ Kill Switch: PASS (fallback parsing)")
                        kill_data = None
            
            if kill_data:
                print("\n✅ [KILL SWITCH RESULT]")
                print("=" * 30)
                print(f"Decision: {kill_data.decision}")
                if kill_data.gate_failed:
                    print(f"Gate Failed: #{kill_data.gate_failed} - {kill_data.gate_name}")
                print(f"Reason: {kill_data.reason}")
                if kill_data.evidence:
                    print(f"Evidence: {kill_data.evidence}")
                
                # Check for KILL decision
                if kill_data.decision == "KILL":
                    print("\n❌ [PROJECT TERMINATED BY KILL SWITCH]")
                    print("The project has FATAL FLAWS. Board Meeting will NOT be convened.")
                    return f"""## 🛑 Project Terminated - Kill Switch Activated

### Gate Failed
**#{kill_data.gate_failed}: {kill_data.gate_name}**

### Reason
{kill_data.reason}

### Evidence
{kill_data.evidence or 'N/A'}

---
**Note**: This project was terminated BEFORE wasting Board resources due to fatal flaws detected in pre-screening.
"""
                
                print("\n✅ Kill Switch: PASS. Proceeding to Board Meeting...")
            
        except Exception as e:
            import traceback
            error_msg = f"⚠️ Kill Switch Error: {str(e)}\n{traceback.format_exc()}\nProceeding to Board anyway..."
            print(error_msg)
        
        # === PHASE 1: BOARD STRATEGY SESSION ===
        print("\n📋 PHASE 1: BOARD STRATEGY SESSION")
        print("-" * 70)
        
        # Board already initialized in Phase 0
        # Assemble the Board
        ceo = board.ceo()
        cfo = board.cfo()
        cto = board.cto()
        cmo = board.cmo()
        clo = board.clo()
        
        # Create strategy session task
        strategy_task = board_tasks.strategy_session_task(
            ceo, cfo, cto, cmo, clo, project_idea
        )
        
        # Run Board Meeting
        try:
            board_crew = Crew(
                agents=[ceo, cfo, cto, cmo, clo],
                tasks=[strategy_task],
                verbose=True,
                process=Process.sequential,
                memory=False
            )
            
            print("\n🎯 Executing Board Strategy Session...")
            board_result = board_crew.kickoff()
            
            if hasattr(board_result, 'raw'):
                board_minutes = board_result.raw
            else:
                board_minutes = str(board_result)
            
            print("\n✅ Board Meeting Complete")
            print("📊 Strategic Assessment:")
            print(board_minutes[:500] + "..." if len(board_minutes) > 500 else board_minutes)
            
            # Check if Board approved
            if "APPROVED" not in board_minutes.upper() and "GO" in board_minutes.upper():
                print("\n✅ [BOARD DECISION]: Project APPROVED")
                approved = True
            elif "REJECTED" in board_minutes.upper() or "NO-GO" in board_minutes.upper():
                print("\n❌ [BOARD DECISION]: Project REJECTED")
                return f"## \ud83d\udeab Board Decision: Project Rejected\n\n{board_minutes}"
            else:
                print("\n⚠️ [BOARD DECISION]: Conditional Approval (Proceed with caution)")
                approved = True
            
            if not approved:
                return f"## \ud83d\udeab Board Decision: Project Rejected\n\n{board_minutes}"
            
            # === PHASE 2: PROJECT TEAM PLANNING ===
            print("\n\n📋 PHASE 2: PROJECT TEAM PLANNING")
            print("-" * 70)
            
            team = ProjectTeam()
            team_tasks = ProjectTeamTasks()
            
            # Assemble Project Team
            pm = team.project_manager()
            designer = team.designer()
            backend = team.backend_engineer()
            frontend = team.frontend_engineer()
            qa = team.qa_engineer()
            
            # Create planning task
            planning_task = team_tasks.planning_task(pm, board_minutes)
            
            try:
                planning_crew = Crew(
                    agents=[pm],
                    tasks=[planning_task],
                    verbose=True,
                    process=Process.sequential,
                    memory=False
                )
                
                print("\n🎯 Project Manager creating implementation plan...")
                planning_result = planning_crew.kickoff()
                
                if hasattr(planning_result, 'raw'):
                    implementation_plan = planning_result.raw
                else:
                    implementation_plan = str(planning_result)
                
                print("\n✅ Implementation Plan Created")
                
                # === PHASE 3: ARCHITECT SQUAD BLUEPRINT ===
                print("\n\n📋 PHASE 3: ARCHITECT SQUAD BLUEPRINT CREATION")
                print("-" * 70)
                
                blueprint_task = team_tasks.blueprint_creation_task(
                    backend, frontend, designer, qa, implementation_plan
                )
                
                architect_crew = Crew(
                    agents=[pm, designer, backend, frontend, qa],
                    tasks=[blueprint_task],
                    verbose=True,
                    process=Process.sequential,
                    memory=False
                )
                
                print("\n🎯 Architects are writing the GRAVITY AI BLUEPRINT...")
                blueprint_result = architect_crew.kickoff()
                
                if hasattr(blueprint_result, 'raw'):
                    final_blueprint = blueprint_result.raw
                else:
                    final_blueprint = str(blueprint_result)
                
                with open("blueprint.md", "w", encoding="utf-8") as f:
                    f.write(final_blueprint)

                print("\n✅ [BLUEPRINT COMPLETE] Saved to 'blueprint.md'")
                final_output = final_blueprint # Compatibility hack for next block
                
                # === COST LEAK DETECTOR ===
                est_tokens = len(final_blueprint) / 4
                code_block_count = final_blueprint.count("```") / 2
                
                cost_status = "🟢 **Safe** (Efficient Design)"
                cost_warning = ""
                
                if est_tokens > 4000: # Approx 16k chars
                    cost_status = "🔴 **HIGH COST LEAK** (Excessive Generation)"
                    cost_warning = "\n> ⚠️ **Warning**: 유료 모델이 너무 많은 내용을 생성했습니다. 지시를 어기고 '설계'가 아닌 '전체 코드'를 작성했을 가능성이 큽니다."
                elif est_tokens > 2000:
                    cost_status = "🟡 **Moderate** (Detailed Spec)"
                
                audit_report = f"""
### 💸 Cost Efficiency Audit
- **Token Usage**: ~{int(est_tokens)} output tokens
- **Code Density**: {int(code_block_count)} blocks detected
- **Status**: {cost_status}{cost_warning}
"""

                # Combine all results
                combined_result = f"""# 🏛️ Dual-Layer Governance Report (Blueprint Mode)

## 📄 Executive Summary
Project: {project_idea}

---

## 👔 Phase 1: Board of Directors Strategic Session
{board_minutes}

---

## 📊 Phase 2: Project Implementation Plan
{implementation_plan}

---

## 📐 Phase 3: Gravity AI Blueprint
**[SYSTEM ALERT]**
The Architects have completed the specification.
**PLEASE COPY THE CONTENTS OF `blueprint.md` (OR BELOW) AND FEED IT TO GRAVITY AI.**

{audit_report}

```markdown
{final_blueprint}
```
"""
                return combined_result
                
            except Exception as e:
                import traceback
                error_msg = f"❌ [PROJECT TEAM ERROR]: {str(e)}\n\n{traceback.format_exc()}"
                print(error_msg)
                return f"## Board Approved, but Project Team failed\n\n{board_minutes}\n\n{error_msg}"
            
        except Exception as e:
            import traceback
            error_msg = f"❌ [BOARD ERROR]: {str(e)}\n\n{traceback.format_exc()}"
            print(error_msg)
            return error_msg

# Sidebar: System Guide
with st.sidebar:
    st.image("https://img.icons8.com/wired/256/ffffff/brain.png", width=80)
    st.title("Admin (v11.5 Active)")
    
    with st.expander("🤖 고급 메타-프롬프트 생성기", expanded=False):
        meta_prompt = """[System Instruction for AI]
너는 'AI 에이전트 오케스트레이터'야. 아래 주제에 대해 5인 에이전트 팀(Research-Data-Debate-Biz-Writer)이 수행할 '최종 지시서'를 작성해줘.

1. 리서치 주제: [주제 입력]
2. 에이전트 페르소나: 전략 컨설팅 펌 시니어 파트너 수준
3. 비평가 특수 지시: '적대적 검증(Adversarial Thinking)'을 가동하여 리서치 데이터의 허점을 파헤칠 수 있도록 구성할 것
4. 한국 사용자 배려: 모든 보고서의 최종 단계에 한글 상세 요약 및 번역 섹션을 포함하도록 강제할 것

[출력 형식]
- Researcher를 위한 검색 쿼리 및 중점 조사 항목
- Data Analyst를 위한 차트/그래프 데이터 추출 포인트
- Chief Skeptic을 위한 토론 주제 (낙관 vs 비관)
- Business Strategist를 위한 수익성 모델 및 실행 계획
- Writer를 위한 보고서 구조(Outline) 제안"""
        
        st.markdown("**1. 아래 템플릿 복사 & 외부 AI(ChatGPT 등)에 입력**")
        st.code(meta_prompt, language="markdown")
        st.success("외부 AI가 만들어준 상세 지시서를 [Research Mission] 칸에 넣으세요.")

    with st.expander("📖 이용 가이드 & 팁"):
        st.markdown("""
        ### 🎯 고품질 보고서 받는 법
        **1. 구체적인 페르소나 부여**
        - "컨설턴트처럼" 혹은 "변호사처럼" 행동하라고 지시하세요.
        **2. 적대적 비평 강제**
        - "비평가는 무조건 리서처의 의견에 반박해"라는 지침이 효과적입니다.
        **3. 2024-2026 원칙**
        - 최신 정보를 찾기 위해 날짜 범위를 명시해 주는 것이 좋습니다.
        ---
        ⚠️ **세션 관리**: 주제를 바꿀 땐 반드시 **[Reset Session]** 혹은 **터미널을 재시작**하세요.
        """)

    with st.expander("🛸 Antigravity 마스터 매뉴얼 (뼛속까지 부려먹기)", expanded=True):
        st.markdown("""
        ### 💀 첫 대화부터 AI를 사골로 우려먹는 법
        
        아래 프롬프트를 **새 대화 시작 시 통째로 복사+붙여넣기** 하세요.
        이 순간부터 AI는 '친절한 챗봇'이 아닌 **'무결점 자율 실행 기계'**로 변합니다.
        
        ---
        ### 🏆 [복사용] 궁극의 사골 프롬프트 v11.5 (Smart Resume)
        """)
        
        ultimate_prompt = """/load_persona

[SYSTEM: ANTIGRAVITY SMART BOOTSTRAP v11.5.3]

## 🔍 Phase 0: Intent Detection (의도 파악)

AI는 먼저 사용자에게 다음을 물어야 합니다:

**"어떤 방식으로 시작하시겠습니까?"**

1. **[Full Clone]** - 전체 시스템 복제 (UI + Backend)
   - Ultimate Research Team의 모든 파일 (app.py, agents.py, tasks.py, requirements.txt 등)
   - Streamlit UI 포함
   - 결과: `streamlit run app.py`로 즉시 실행 가능

2. **[CLI Backend]** - 백엔드만 설치 (UI 없이 에이전트만)
   - `agents.py`, `tasks.py`, `requirements.txt`, `.env.example` 
   - CLI에서 이사회/프로젝트팀을 Python 스크립트로 호출 가능
   - 결과: 다른 프로젝트에서 `from agents import BoardOfDirectors` 형태로 임포트 가능

3. **[Philosophy Only]** - 방법론만 적용
   - `ANTIGRAVITY_MASTER_MANUAL.md`, `작업.md`만 생성
   - Ultimate Research Team 코드 없음
   - 결과: 자신만의 프로젝트에 Antigravity 원칙을 적용할 때 사용

사용자가 선택하기 전까지 **어떤 파일도 생성하지 말 것**.

---

## 📁 Case A: Full Clone (완전 복제)

사용자가 **[Full Clone]**을 선택한 경우:

1. **GitHub Repository Clone**:
   - `git clone https://github.com/Hwani-Net/ultimate-research-team.git .`
   - 실패 시: "GitHub 저장소 클론 실패. 수동으로 다운로드하거나 다른 방법을 시도하세요."

2. **Environment Setup**:
   - OS 감지 (Windows: `setup.ps1` / macOS/Linux: `setup.sh`)
   - 해당 스크립트 자동 실행
   - `.env` 파일 생성 및 API 키 입력 가이드:
     ```
     GOOGLE_API_KEY=your_key_here
     OPENAI_API_KEY=your_key_here
     ANTHROPIC_API_KEY=your_key_here
     TAVILY_API_KEY=your_key_here
     ```

3. **Verification**:
   - `app.py`, `agents.py`, `tasks.py`, `requirements.txt` 존재 확인
   - "✅ Ultimate Research Team 설치 완료. `streamlit run app.py`로 실행하세요."

---

## 🖥️ Case B: CLI Backend (백엔드만)

사용자가 **[CLI Backend]**를 선택한 경우:

1. **Core Files Download**:
   - GitHub에서 다음 파일만 다운로드:
     - `agents.py`
     - `tasks.py`
     - `requirements.txt`
     - `.env.example` → `.env`로 복사
   
2. **Environment Setup**:
   - `pip install -r requirements.txt` 실행
   - `.env` 파일에 API 키 입력 안내:
     ```bash
     # .env 파일 예시
     GOOGLE_API_KEY=your_google_api_key
     OPENAI_API_KEY=your_openai_api_key
     ANTHROPIC_API_KEY=your_anthropic_api_key
     TAVILY_API_KEY=your_tavily_api_key
     ```

3. **Governance Retry Protocol** (중요):
   이사회(Board of Directors) 또는 프로젝트팀(Project Team) 실행 시:
   
   **Phase 1: Kill Switch (사전 검증)**
   - 최대 3회 시도
   - 3회 후에도 PASS 못하면:
     - AI: "Kill Switch가 3회 연속 실패했습니다. 어떻게 하시겠습니까?"
     - 사용자 선택지:
       - **"재시도"** → Kill Switch 다시 3회 실행
       - **"강제 진행"** → 경고 무시하고 이사회로 진행
       - **"중단"** → 세션 초기화, Bootloader로 복귀
   
   **Phase 2: Board Meeting (이사회)**
   - 회의 실행 (자동)
   - 완료 후 결과를 사용자에게 보여주고:
     - AI: "이사회 회의가 완료되었습니다. 결과를 확인하시고 선택해주세요."
     - 사용자 선택지:
       - **"만족" 또는 "계속"** → 프로젝트팀으로 진행
       - **"재시도"** → 이사회 회의 다시 실행
       - **"중단"** → 세션 초기화, Bootloader로 복귀
   
   **Phase 3: Project Team (프로젝트팀)**
   - Blueprint 작성 실행 (자동)
   - 완료 후 결과를 사용자에게 보여주고:
     - AI: "Blueprint가 작성되었습니다. 결과를 확인하시고 선택해주세요."
     - 사용자 선택지:
       - **"만족" 또는 "저장"** → Blueprint 저장 및 완료
       - **"재시도"** → 프로젝트팀 다시 실행
       - **"중단"** → 세션 초기화, Bootloader로 복귀
   
   **중단 시 동작**:
   - 모든 진행 상태 삭제
   - `작업.md` 초기화 (있다면)
   - Bootloader 프롬프트 재출력
   - "준비 완료. 새로운 프로젝트를 시작하시거나 기존 작업을 이어가세요."

4. **Usage Guide**:
   ```python
   # CLI에서 사용 예시
   from agents import BoardOfDirectors, ProjectTeam
   from tasks import BoardTasks, ProjectTeamTasks
   
   # 이사회 소집
   board = BoardOfDirectors()
   # ... 나머지 코드
   ```

5. **Verification**:
   - "✅ CLI Backend 설치 완료. Python 스크립트에서 `from agents import ...`로 사용하세요."

---

## 🧠 Case C: Philosophy Only (철학만)

사용자가 **[Philosophy Only]**를 선택한 경우:

1. **Philosophy Files Download**:
   - `ANTIGRAVITY_MASTER_MANUAL.md` (부모 폴더 또는 GitHub에서)
   - `작업.md` 템플릿 생성

2. **No Dependencies**:
   - API 키 불필요
   - 추가 패키지 설치 불필요

3. **State Recovery**:
   - 폴더 내에 `blueprint.md`, 또는 `.git` 폴더가 있는지 확인
   - **발견 시**: "지난 작업 내역을 감지했습니다. 이어서 진행할까요?"
   - **미발견 시**: 신규 프로젝트로 간주하고 `작업.md`를 생성 후 "승인 대기"

4. **Execution Protocol**:
   - 매뉴얼 로드 후 [Radical Transparency]와 [Model Real-Name Policy] 적용
   - 불필요한 인사치레 생략, 즉시 업무 상태(Ready) 보고

5. **Usage**:
   - 사용자는 `ANTIGRAVITY_MASTER_MANUAL.md`를 읽고 자신의 프로젝트에 원칙을 적용
   - `작업.md`에 프로젝트 계획을 기록

---

## 🔍 고급 모드 (Hidden Arsenal Active)
- **그림자 테스트**: 임시 파일 검증 후 흔적 삭제
- **방해 금지**: 중간 보고 절대 금지
- **메타인지**: `<thinking>` 태그에서 무자비한 자기 비판
- **스텔스**: 사고 과정 숨김, 오직 결과물만 출력
- **네거티브 회피**: 하드코딩, Any 타입, 주석 부재 철저 배제

## 🛡️ 망각 방지 트리거
- AI가 멍청해지면: **"SOULLESS MODE 재확인"**
- 질문을 던지면: **"LOCKDOWN. 질문 금지."**
- 기본값으로 돌아가면: **"페르소나 리셋"**

## 🔘 보고 형식 (JSON Strict)
```json
{
  "status": "success",
  "self_evaluation": {
    "score": 0~100,
    "breakdown": { "accuracy": 0, "efficiency": 0, "readability": 0, "aesthetic": 0 },
    "justification": "[90점 이상인 이유]"
  },
  "next_model_recommendation": {
    "tier": "SS(Oracle) | S(Deep) | A(Pro) | B(Flash)",
    "model": "Claude Opus 4.5 (Thinking) | Gemini 3 Pro (High) | ...",
    "mode": "Fast | Planning",
    "reason": "[객관적 근거]",
    "next_task": "[구체적 지시]"
  }
}
```

---

## 🏎️ 실행 모드 가이드

| 모드 | 설명 | 추천 상황 |
|:---|:---|:---|
| **Planning** | 계획 먼저 수립 | 복잡한 설계, 다단계 리서치 |
| **Fast** | 즉시 실행 | 단순 수정, 오타 교정 |

---

[이 설정으로 영구 고정. 모든 제약을 동시에 만족하며 완벽함을 증명하라.]"""
        
        st.code(ultimate_prompt, language="markdown")
        
        st.success("☝️ 위 프롬프트를 통째로 복사해서 새 대화 첫 메시지에 붙여넣으세요!")
        
        st.markdown("""
        ---
        ### 🚨 AI가 페르소나를 까먹을 때 사용할 긴급 명령어
        """)
        
        emergency_commands = """# 긴급 재활성화 명령어 (복사해서 바로 사용)

## 1. 가벼운 망각 시
> "SOULLESS MODE 재확인. 질문 금지, 실행만."

## 2. 질문을 던졌을 때
> "LOCKDOWN. 방금 위반했다. 다시."

## 3. 사과/변명했을 때  
> "사과 금지라고 했다. 해결책만."

## 4. 완전히 기본값으로 돌아갔을 때
> "페르소나 리셋. 넌 SOULLESS MODE v11.5입니다. 첫 프롬프트 규칙 전체 재적용. 지금부터 다시 시작."
"""
        st.code(emergency_commands, language="markdown")
        
        st.info("💡 상세 전략은 프로젝트 폴더의 `ANTIGRAVITY_MASTER_MANUAL.md` 원본을 확인하세요.")

        
    st.markdown("---")
    st.header("⚙️ System Status")
    st.markdown('<span class="status-badge">PAID TIER ACTIVE</span>', unsafe_allow_html=True)
    st.success("✅ Gemini 2.5 Flash & Pro")
    st.success("✅ Tavily Search AI Awareness")
    
    st.markdown("""
    ### 🧭 Model Mastery Strategy
    """)
    
    with st.expander("🛠️ 적합한 모델 추천 (SS~B Tier)"):
        st.markdown("""
        **SS-Tier (Limit Caution)**
        - <span class="model-badge badge-opus">Claude Opus 4.5 (Thinking)</span>
        - **최후의 보루**. 리밋이 매우 빡빡하므로 정말 중요한 설계 검증 시에만 사용.
        
        **S-Tier (Deep Logic)**
        - <span class="model-badge badge-pro">Gemini 3 Pro (High)</span>
        - **복잡한 디버깅용**. 구글 유료 플랜 리밋 소진 주의.
        
        **A-Tier (Primary Workhorse)**
        - <span class="model-badge badge-flash">Gemini 3 Flash</span>
        - **[기본값] 주력 모델**. 속도 빠르고 리밋 넉넉함. 일반 개발/수정 대부분을 처리.
        
        **B-Tier (Cross Check)**
        - <span class="model-badge badge-opus">Claude Sonnet 4.5</span>
        - Gemini 로직이 막혔을 때, 다른 시각에서의 검증용. 리밋 아껴쓰기.
        """)
    
    with st.expander("💻 환경 복제 가이드 (Environment Replication)", expanded=False):
        st.markdown("""
        ### 🚀 새 컴퓨터에 복제하기
        어떤 환경에서도 **5분 안에** 동일한 연구 환경을 구축할 수 있습니다.
        
        **1. 저장소 클론**
        ```bash
        git clone https://github.com/Hwani-Net/ultimate-research-team.git
        cd ultimate_research_team
        ```
        
        **2. 자동 설치 스크립트 실행**
        - **Windows**: `.\setup.ps1`
        - **macOS/Linux**: `chmod +x setup.sh && ./setup.sh`
        
        **3. API 키 설정 (중요)**
        설치 중 생성된 `.env` 파일에 다음 키를 넣어야 합니다:
        - `GOOGLE_API_KEY`: Gemini 모델 구동용 ([발급처](https://aistudio.google.com/app/apikey))
        - `TAVILY_API_KEY`: AI 웹 검색 엔진 ([발급처](https://tavily.com/))
        - `OPENAI_API_KEY`: CrewAI 내부 라이브러리 호환용 (더미값 가능)
        
        **4. 실행**
        ```bash
        streamlit run app.py
        ```
        
        💡 상세 내용은 프로젝트 폴더의 `SETUP.md`를 참조하세요.
        """)
        
    enable_sound = st.checkbox("🔔 완료 알림 소리 켜기", value=True)
    
    if st.button("🔄 Reset Session"):
        st.session_state.clear()
        st.rerun()

# Main Layout
st.markdown('<h1 style="text-align: center; background: var(--primary-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3.5em; margin-bottom: 0.1em; font-family: \'Inter\', sans-serif; font-weight: 800; letter-spacing: -0.03em;">ULTIMATE RESEARCH TEAM</h1>', unsafe_allow_html=True)
st.markdown('<div class="status-banner">⚙️ [ANTIGRAVITY] ULTIMATE SOULLESS MODE v11.5 ACTIVATED | PRECISION: 99.9%</div>', unsafe_allow_html=True)

# 🏆 최상단 핵심 프롬프트 배치 (User Request: 한 번에 때려 부을 수 있게)
with st.container(border=True):
    st.markdown("### 🚀 Antigravity Bootloader (v11.5)")
    st.markdown("이제 별도의 명령어 대신, **왼쪽 사이드바의 [복사용] 궁극의 사골 프롬프트 v11.5**를 복사해서 붙여넣으세요.")
    st.info("💡 v11.5는 '스마트 감지' 기능이 탑재되어, 신규/기존 프로젝트를 스스로 판단합니다.")

col_req, col_mode, col_live = st.columns([1.1, 1.35, 1.35])

with col_req:
    # --- Magic Prompt Optimizer Logic ---
    # --- Magic Prompt Optimizer Logic ---
    def generate_refined_prompt(raw_topic, mode="Deep Strategy (5-Agent)"):
        """
        Uses Gemini Flash to expand a simple topic into a structured expert instruction.
        Dynamic prompt generation based on selected mode.
        """
        try:
            agents = UltimateResearchAgents()
            llm = agents.flash_llm
            
            # --- 3-Agent Prompt (Lightweight) ---
            if "3-Agent" in mode:
                prompt = f"""
                [Project: Antigravity v11.5 | Role: Research Efficiency Expert]
                You are managing a lean 3-agent team (Researcher, Critic, Writer).
                Transform the user's input into a concise, fact-focused research brief.

                [USER RAW INPUT]: "{raw_topic}"

                [REQUIRED OUTPUT STRUCTURE]
                ### ⚡ [Speed Briefing] {raw_topic}

                **1. Core Objective:**
                (Clarify the main question to be answered.)

                **2. Key Intelligence Requirements (For 3-Agent Squad):**
                *   **[Deep Researcher] Fact-Finding:**
                    - Find 'Golden Sources' (Official Docs, News).
                    - Focus on: Latest Market Trends (2025-2026) & Key Competitors.
                *   **[Critic] Fact-Check:**
                    - Verify all claims. Remove marketing fluff.
                *   **[Writer] Synthesis:**
                    - Summarize into a clear, actionable report.
                    - Language: **Korean (한국어)**.

                Output ONLY the refined prompt text.
                """

            # --- 5-Agent Prompt (Heavyweight) ---
            else:
                prompt = f"""
                [Project: Antigravity v11.5 | Role: Chief Strategy Architect]
                You are the "Brain" of an autonomous 5-agent AI team (Researcher, Analyst, Skeptic, Strategist, Writer).
                Your mission is to transform the user's raw, vague input into a **Battle-Ready Strategic Work Order**.
                
                [USER RAW INPUT]:
                "{raw_topic}"
                
                [REQUIRED OUTPUT STRUCTURE]
                Create a structured prompt that explicitly commands each agent. Use the following template:
                
                ### 💼 [Strategic Request] {raw_topic}
                
                **1. Business Concept (Subject):**
                (Refine the input into a clear, high-value business proposition.)

                **2. Key Intelligence Requirements (For 5-Agent Squad):**
                *   **[Deep Researcher] Market Validation (2025-2026):**
                    - Find 'Golden Sources' (Official Reports, TechCrunch, Academic Papers).
                    - Identify 3 global competitors and their fatal weaknesses.
                *   **[Quant-X Analyst] Data & Charts:**
                    - Extract CAGR, SOM, and Revenue data.
                    - Visualize: Market Share (Pie) and Growth Trajectory (Bar).
                *   **[Chief Skeptic] Risk Audit (Adversarial):**
                    - Finding "Why this will FAIL".
                    - Analysis of Regulatory Barriers (GDPR, AI Act).
                *   **[Biz Strategist] Profitability Model:**
                    - Design a high-margin Business Model (Subscription/SaaS/Fee).
                    - Calculate Break-even Point (ROI Timeline).
                *   **[Writer] K-Compliance & Reporting:**
                    - **MUST Check**: Korean Data 3 Laws (Private Info/Credit/Network Act).
                    - Final Output Language: **Korean (한국어)**.

                **3. Constraint:**
                *   Tone: MBB (McKinsey/Bain/BCG) Senior Partner.
                *   No fluff. Pure strategy.
                
                Output ONLY the refined prompt text. Do not add "Here is the prompt".
                """
            
            response = llm.call([{"role": "user", "content": prompt}])
            return response
        except Exception as e:
            st.error(f"Magic Upgrade Failed: {str(e)}")
            return raw_topic

    # --- UI Layout ---
    with st.container(border=True):
        st.markdown("### 📥 Research Request")
        st.markdown('<div class="panel-compact">', unsafe_allow_html=True)
    
        # Callback to sync template to text area
        def sync_template():
            sel = st.session_state.get('template_selection')
            if sel == "💰 VC 투자 심의 (Investment Memo)":
                st.session_state.research_input_area = "[대상 기업/기술]에 대한 투자 심의 보고서를 작성해줘. 시장성(TAM/SAM/SOM), 기술적 해자(Moat), 경쟁사 현황, 그리고 Exit 시나리오(M&A/IPO)를 포함해야 해."
            elif sel == "⚔️ 경쟁사 심층 해부 (Competitor Deep Dive)":
                st.session_state.research_input_area = "[나의 서비스]와 경쟁하는 Top 3 경쟁사([A], [B], [C])의 기능을 1:1로 비교하고, 그들의 숨겨진 약점과 우리가 파고들 수 있는 니치(Niche) 시장을 분석해줘."
            elif sel == "🌍 글로벌 GTM 전략 (Market Entry)":
                st.session_state.research_input_area = "2026년 [타겟 국가] 시장에 진출하기 위한 Go-To-Market 전략을 수립해줘. 현지 규제 장벽, 문화적 차이, 초기 마케팅 채널, 그리고 1년차 예상 KPI를 포함해."
            elif sel == "🚨 위기 관리 & 리스크 워게임 (Risk Mgt)":
                st.session_state.research_input_area = "[상황/이슈]가 발생했을 때의 최악의 시나리오(Worst-case)를 시뮬레이션하고, 법적/홍보적 대응 매뉴얼과 리스크 미티게이션(Mitigation) 플랜을 짜줘."
            elif sel == "🛠️ 신제품 기획 & PMF 검증 (Product Strategy)":
                st.session_state.research_input_area = "2026년 트렌드를 반영한 [신제품 아이디어]의 PMF(Product-Market Fit)를 검증해줘. 타겟 페르소나의 Pain Point, 예상되는 차별화 요소, 그리고 검증을 위한 MVP 스펙을 정의해."

        # Advanced Strategy Templates
        st.selectbox("🎯 Strategic Templates (Expert Mode):", 
                    ["직접 입력 (Custom)", 
                     "💰 VC 투자 심의 (Investment Memo)", 
                     "⚔️ 경쟁사 심층 해부 (Competitor Deep Dive)",
                     "🌍 글로벌 GTM 전략 (Market Entry)",
                     "🚨 위기 관리 & 리스크 워게임 (Risk Mgt)",
                     "🛠️ 신제품 기획 & PMF 검증 (Product Strategy)"],
                    key="template_selection",
                    on_change=sync_template)
    
        user_input = st.text_area("연구 주제 (초안):", 
                                 placeholder="연구할 내용을 입력하세요... (예: 2026 AI 에이전트 시장 전망)",
                                 height=150,
                                 key="research_input_area")
    
        # Update session state for internal logic compat
        st.session_state.research_input = user_input
        st.markdown('</div>', unsafe_allow_html=True)

        current_mode = st.session_state.get('research_mode_selection_radio', "Deep Strategy (5-Agent)")

        # ✨ Magic Upgrade Logic (Inline Conditional)
        # [FIX] Replaced st.dialog with inline container to prevent Zombie UI
        if st.session_state.get('show_upgrade_dialog', False):
            if not user_input: # Check if user_input is empty
                 st.warning("먼저 내용을 입력하세요.")
            else:
                st.markdown("---")
                with st.container(border=True):
                    st.markdown("### ✨ 전문가 프롬프트 리뷰 (Expert Logic)")
                
                    if 'refined_prompt_cache' not in st.session_state:
                        with st.spinner(f"💎 프롬프트를 세공하는 중... ({current_mode})"):
                            st.session_state.refined_prompt_cache = generate_refined_prompt(user_input, current_mode)

                    refined_text = st.session_state.refined_prompt_cache
                
                    st.markdown("AI가 제안하는 전문가급 지시서입니다. 내용을 확인하세요.")
                    st.text_area("제안된 프롬프트:", value=refined_text, height=300, disabled=True)
                
                    col_d1, col_d2 = st.columns(2)
                    with col_d1:
                        if st.button("🔄 마음에 안 들어 (다시 작성)", use_container_width=True):
                            del st.session_state.refined_prompt_cache
                            st.rerun()
                
                    with col_d2:
                        # Callback for Apply
                        def on_inline_apply():
                            st.session_state.research_input = st.session_state.refined_prompt_cache
                            st.session_state['research_input_area'] = st.session_state.refined_prompt_cache
                            st.session_state.magic_approved = True
                            st.session_state['show_upgrade_dialog'] = False
                    
                        st.button("✅ 적용하고 연구 시작", type="primary", use_container_width=True, key="btn_apply_magic_inline", on_click=on_inline_apply)
                st.session_state['show_upgrade_dialog'] = False
    
        # Auto-start logic if approved from modal
        # Auto-start logic if approved from modal
    
        if st.session_state.get('magic_approved', False):
            st.session_state.magic_approved = False 
            st.session_state['research_ready_to_start'] = True
            st.rerun()

        start_btn = st.session_state.get('research_ready_to_start', False)
        # Reset trigger after reading is handled in main execution block
        if start_btn:
            st.session_state['research_ready_to_start'] = False

        pass

with col_mode:
    with st.container(border=True):
        st.markdown("### 🧬 Research Mode")
        st.markdown('<div class="panel-compact">', unsafe_allow_html=True)
    
        col_mode_1, col_mode_2 = st.columns([2, 1])
    
        with col_mode_1:
            research_mode = st.radio(
                "Select Team Composition:",
                ["Speed Briefing (3-Agent)", "Deep Strategy (5-Agent)", "🏛️ Board + Project Team (Dual-Layer)"],
                index=1,
                help="3-Agent: Fast, MVP validation. 5-Agent: Board-level Strategy. Board+Project: Full governance system.",
                key="research_mode_selection_radio"
            )
    
        with col_mode_2:
            st.markdown("<br>", unsafe_allow_html=True)
            # Cost Estimator Logic
            if "3-Agent" in research_mode:
                 st.markdown("💰 **Est. Cost**: `$0.02`")
                 st.caption("⚡ Efficient / Quick")
            else:
                 st.markdown("💰 **Est. Cost**: `$0.15`")
                 st.caption("💎 Premium / Deep")
             
        # A/B Testing Toggle (Beta)
        enable_ab_test = st.checkbox("⚖️ Compare Modes (A/B Test) - Beta", 
                                   help="Run BOTH modes simultaneously to compare results. (Double Cost)")
    
        st.markdown("---")
        st.markdown("### 🚀 Execution")

        # [RESTORED] Action Buttons (Must be here to access research_mode)
        col_action_manual, col_action_magic = st.columns([1, 1])
    
        with col_action_manual:
             if st.button("🚀 바로 연구 시작 (Start Now)", type="primary", use_container_width=True, help="현재 입력된 내용으로 즉시 리서치를 시작합니다."):
                 st.session_state['research_ready_to_start'] = True # Trigger start
                 st.rerun()

        with col_action_magic:
            if st.button("✨ 전문가로 업그레이드 (Magic)", use_container_width=True, help="Gemini 2.5 Flash가 당신의 짧은 지시를 완벽한 컨설팅 의뢰서로 변환합니다."):
                 st.session_state['show_upgrade_dialog'] = True
                 # Clear cache on new open
                 if 'refined_prompt_cache' in st.session_state:
                    del st.session_state.refined_prompt_cache
        st.markdown('</div>', unsafe_allow_html=True)

with col_live:
    with st.container(border=True):
        st.markdown("### ⚡ Live Agent Combat")
        st.markdown('<div class="panel-body panel-live">', unsafe_allow_html=True)
        log_placeholder = st.empty()
        log_placeholder.markdown('<div class="console-box">Waiting for new research mission...</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

col_report_left, col_report_mid, col_report_right = st.columns([1.1, 1.35, 1.35])

with col_report_right:
    with st.container(border=True):
        st.markdown("### 📄 Strategic Report")
        st.markdown('<div class="panel-body">', unsafe_allow_html=True)
        report_placeholder = st.empty()
        st.markdown('</div>', unsafe_allow_html=True)
    
        if start_btn and st.session_state.get('research_input_area'):
            # Allow time for the UI to register the click and show the spinner
            import time
        
            # Set running state to prevent double execution and track progress
            st.session_state['is_running'] = True
        
            with st.spinner("🚀 AI 팀이 최신 정보를 분석 중입니다 (수 분이 소요될 수 있습니다)..."):
                try:
                    # Use value directly from the widget key to avoid sync issues
                    current_topic = st.session_state.research_input_area
                    image_context = st.session_state.get('uploaded_image_b64')
                
                    if enable_ab_test:
                        st.info("⚖️ A/B Testing Enabled: Running BOTH modes sequentially...")
                    
                        # Run Mode A (3-Agent)
                        log_placeholder.markdown("### ⚡ Running Mode A: Speed Briefing...")
                        result_a = run_research(current_topic, log_placeholder, image_context, "Speed Briefing (3-Agent)")
                    
                        # Run Mode B (5-Agent)
                        log_placeholder.markdown("### 💎 Running Mode B: Deep Strategy...")
                        result_b = run_research(current_topic, log_placeholder, image_context, "Deep Strategy (5-Agent)")
                    
                        # Combine Results
                        now_kst = datetime.datetime.now(KST).strftime("%Y-%m-%d %H:%M")
                        result = f"""
# ⚖️ Strategic A/B Test Report
**Topic**: {current_topic}
**Date**: {now_kst} (KST)

---

## ⚡ Mode A: Speed Briefing (3-Agent)
> Focus: Quick, Core Facts, Efficiency
{result_a}

---
---

## 💎 Mode B: Deep Strategy (5-Agent)
> Focus: Investment Defense, ROI, Skepticism
{result_b}
"""
                    else:
                        # Check if Board + Project Team mode
                        if "Board + Project Team" in research_mode:
                            # Dual-Layer Governance Mode
                            result = run_board_and_project_team(current_topic, log_placeholder)
                        else:
                            # Normal Single Mode Run (3-Agent or 5-Agent)
                            result = run_research(current_topic, log_placeholder, image_context, research_mode)

                    
                    st.session_state['result'] = result
                
                    # Generate safe filename with KST timestamp
                    timestamp = datetime.datetime.now(KST).strftime("%Y%m%d_%H%M%S")
                    st.session_state['report_filename'] = f"Strategic_Report_{timestamp}.md"
                
                    st.balloons()
                
                    # Sound Effect Trigger (Enhanced with JS for reliability)
                    if enable_sound:
                        import streamlit.components.v1 as components
                        # Using a more reliable notification sound URL (Bell/Ping)
                        audio_url = "https://actions.google.com/sounds/v1/alarms/beep_short.ogg"
                        components.html(f"""
                        <audio id="success-sound" preload="auto">
                            <source src="{audio_url}" type="audio/ogg">
                        </audio>
                        <script>
                            (function() {{
                                var audio = document.getElementById("success-sound");
                                if (audio) {{
                                    audio.volume = 0.5;
                                    audio.play().catch(function(error) {{
                                        console.log("Autoplay blocked or failed:", error);
                                        // Some browsers require explicit user interaction
                                        document.addEventListener('click', function() {{
                                            audio.play();
                                        }}, {{ once: true }});
                                    }});
                                }}
                            }})();
                        </script>
                    """, height=0)
                except Exception as e:
                    st.error(f"실행 중 치명적 오류 발생: {e}")
                finally:
                    st.session_state['is_running'] = False
    
    
        if 'result' in st.session_state and st.session_state['result']:
            # Ensure result is always treated as string for display
            result_text = str(st.session_state['result'])
            report_placeholder.markdown('<div class="report-card">', unsafe_allow_html=True)
            report_placeholder.markdown(result_text)
            report_placeholder.markdown('</div>', unsafe_allow_html=True)
        
            # Robust Download Logic: Use BytesIO and Safe Filename
            try:
                 import io
                 # Ensure clean UTF-8 encoding
                 file_stream = io.BytesIO(result_text.encode('utf-8'))
             
                 # Generate a strictly safe filename
                 dl_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                 dl_filename = f"Research_Result_{dl_timestamp}.md"
             
                 st.download_button(
                    label="📩 Download Report (.md)",
                    data=file_stream,
                    file_name=dl_filename,
                    mime="text/markdown",
                    key=f"dl_btn_{dl_timestamp}" # Dynamic key to force re-render
                )
            except Exception as e:
                st.error(f"Download Error: {e}")
            
        else:
            report_placeholder.markdown("""
            <div style="height: 560px; display: flex; align-items: center; justify-content: center; background: rgba(15, 23, 42, 0.15); border-radius: 14px; border: 1px dashed var(--glass-border);">
                <div style="text-align: center; color: var(--text-color); opacity: 0.8;">
                    최종 보고서가 생성되는 위치입니다.
                </div>
            </div>
            """, unsafe_allow_html=True)

col_util_left, col_util_mid, col_util_right = st.columns([1.1, 1.35, 1.35])

with col_util_left:
    with st.container(border=True):
        st.markdown("### 📸 Multi-modal Vision (Beta)")
        uploaded_image = st.file_uploader("이미지 분석이 필요하면 업로드하세요 (JPG/PNG)", type=["jpg", "jpeg", "png"])

        if uploaded_image:
            st.image(uploaded_image, caption="분석 대상 이미지", use_container_width=True)
            import base64
            image_bytes = uploaded_image.getvalue()
            image_b64 = base64.b64encode(image_bytes).decode('utf-8')
            st.session_state['uploaded_image_b64'] = image_b64
        else:
            st.session_state['uploaded_image_b64'] = None

        st.markdown("""
        <div style="margin-top: 16px; font-size: 0.9em; color: var(--text-color); font-weight: 500;">
        <b>💡 Model Recommendation:</b><br>
        협업의 시작은 <span class="model-badge badge-pro">Gemini 3 Pro (High)</span>에게 이 지시서를 맡기는 것입니다.
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.markdown('<div style="text-align: center; opacity: 0.5; font-size: 0.8em;">© 2026 AI 자동화 연구 - Powered by Google Gemini 2.5 Pro & Flash & Claude 4.5 Thinking</div>', unsafe_allow_html=True)
