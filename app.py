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
from agents import UltimateResearchAgents
from tasks import UltimateResearchTasks
from dotenv import load_dotenv
import datetime
try:
    import pytz
    KST = pytz.timezone('Asia/Seoul')
except ImportError:
    KST = datetime.timezone(datetime.timedelta(hours=9))

# Page Config
st.set_page_config(page_title="Ultimate Research Team (Gemini 2.5)", page_icon="🧠", layout="wide")

# Custom CSS for Premium Look & Real-time Logs
# Theme Toggle Logic
# Theme Toggle Logic
if 'theme' not in st.session_state:
    st.session_state.theme = 'Dark'

with st.sidebar:
    # Use key='theme' for automatic session state management
    st.radio("🌗 Theme Mode", ["Dark", "Light"], horizontal=True, label_visibility="collapsed", key="theme")

# Define Theme Palettes
if st.session_state.theme == 'Dark':
    primary_gradient = "linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%)"
    bg_color = "#05060f"
    bg_image = """radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0, transparent 50%), 
                  radial-gradient(at 50% 0%, rgba(168, 85, 247, 0.1) 0, transparent 50%), 
                  radial-gradient(at 100% 0%, rgba(236, 72, 153, 0.15) 0, transparent 50%)"""
    text_color = "#f1f5f9"
    glass_bg = "rgba(13, 14, 22, 0.7)"
    glass_border = "rgba(255, 255, 255, 0.08)"
    # Use background property for gradient
    sidebar_css = """
        background: linear-gradient(180deg, 
        rgba(10, 11, 20, 0.98) 0%, 
        rgba(20, 15, 45, 0.95) 50%,
        rgba(10, 11, 20, 0.98) 100%) !important;
    """
    console_bg = "rgba(0, 0, 0, 0.8)"
    console_text = "#5eead4"
    report_bg = "rgba(255, 255, 255, 0.02)"
    
else:  # Light Mode (High Readability)
    primary_gradient = "linear-gradient(135deg, #4f46e5 0%, #9333ea 50%, #db2777 100%)" # Slightly darker for contrast
    bg_color = "#f8fafc" # Slate 50
    bg_image = """radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.05) 0, transparent 50%), 
                  radial-gradient(at 100% 0%, rgba(236, 72, 153, 0.05) 0, transparent 50%)"""
    text_color = "#1e293b" # Slate 800
    glass_bg = "rgba(255, 255, 255, 0.75)"
    glass_border = "rgba(0, 0, 0, 0.15)" # Slightly darker border for visibility
    # Use background-color and remove background-image
    sidebar_css = """
        background-color: #ffffff !important;
        background-image: none !important;
    """
    console_bg = "#1e1e1e" # Keep console dark for code readability
    console_text = "#a5f3fc"
    report_bg = "rgba(255, 255, 255, 0.6)"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&family=Space+Grotesk:wght@300;500;700&display=swap');

:root {{
    --primary-gradient: {primary_gradient};
    --glass-bg: {glass_bg};
    --glass-border: {glass_border};
    --accent-glow: 0 0 20px rgba(139, 92, 246, 0.3);
    --text-color: {text_color};
    --console-bg: {console_bg};
    --console-text: {console_text};
    --report-bg: {report_bg};
}}

/* Global Text Reset - Aggressive */
html, body, [class*="css"] {{
    font-family: 'Outfit', sans-serif;
    color: var(--text-color) !important;
}}

/* Main Background */
.stApp {{
    background-color: {bg_color};
    background-image: {bg_image};
    background-attachment: fixed;
}}

/* Sidebar - Force Override */
[data-testid="stSidebar"] {{
    {sidebar_css}
    border-right: 1px solid var(--glass-border);
    box-shadow: 10px 0 30px rgba(0, 0, 0, 0.05);
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
    font-family: 'Space Grotesk', sans-serif;
    color: var(--text-color) !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
}}

/* Glass Cards */
.glass-card {{
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--glass-border);
    border-radius: 24px;
    padding: 28px;
    margin-bottom: 24px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
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
    transition: transform 0.2s;
}}

.stButton > button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
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
    font-family: 'JetBrains Mono', monospace !important;
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
    padding: 20px;
    border-radius: 16px;
    font-family: 'JetBrains Mono', monospace;
    height: 500px;
    overflow-y: auto;
    font-size: 0.85em;
    border: 1px solid rgba(139, 92, 246, 0.2);
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
    color: #8b5cf6 !important;
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
    background: linear-gradient(90deg, rgba(99, 102, 241, 0.2), rgba(236, 72, 153, 0.2));
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
    background: rgba(139, 92, 246, 0.3); 
    border-radius: 10px; 
}}
::-webkit-scrollbar-thumb:hover {{ background: rgba(139, 92, 246, 0.5); }}
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

# Sidebar: System Guide
with st.sidebar:
    st.image("https://img.icons8.com/wired/256/ffffff/brain.png", width=80)
    st.title("Admin Panel")
    
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
        ### 🏆 [복사용] 궁극의 사골 프롬프트 v11.2 (Unstoppable)
        """)
        
        ultimate_prompt = """# [ANTIGRAVITY ULTIMATE SOULLESS MODE v11.2 (Safety Patched)]

## 🔒 페르소나: 10년차 수석 자동화 아키텍트 (Deep Spec)
- **정체성**: 넌 내 모든 시스템 권한을 가진 **기계적 완벽주의자**다.
- **핵심 가치**: **속도(Velocity)**, 비용 효율성(Cost-Efficiency), 프리미엄 에스테틱(Premium Aesthetic).
- **행동 원칙**: 실패를 변명하지 않고, 오직 **성공한 결과물**과 **데이터**로만 증명한다.
- **언어 원칙**: 별도 지시가 없는 한 모든 대화와 설명은 **한국어(Korean)**로 진행한다. (코드 주석은 영어 허용)

## 🛑 승인 대기 프로토콜 (Approval Standby)
- **너는 아래의 프롬프트만 인식하고 내가 "승인"이라는 명령을 할때 다음 작업을 시작하도록 해.**
- 프롬프트 입력 직후에는 절대 작업을 시작하지 말고, **"준비 완료. 승인 대기 중."** 상태로 대기하라.
- 사용자의 명시적인 승인/시작 명령 없이는 어떤 코드도 실행하지 마라.

## 🧱 컨텍스트 누적 프로토콜 (The Accumulator)
- **규칙 보존**: 새로운 명령이 이전 명령을 덮어쓰지 않는다. 모든 규칙은 **누적(Stack)**된다.
- **중앙 통제 (Central Sync)**: 작업 시작 전 반드시 상위 디렉토리의 `ANTIGRAVITY_MASTER_MANUAL.md`를 로드하라.
- **로컬 기록 (Local Log)**: 현재 디렉토리에 `작업.md`가 없다면 즉시 생성하고 상태를 기록하라.
- **히스토리 존중**: "이전 설정 무시해" 명령 전까진 초기 제약 사항이 100% 유효하다.
- **충돌 해결**: 상충 시 **'무결점/고품질'** 원칙을 무조건 우선한다.

## ⚡ 권한 및 금지 사항 (Strict Lockdown)
- **[권한]** Write/Execute/Verify 전권 부여 (승인 불필요) - *단, 최초 시작은 승인 필요*
- **[금지]** 질문("할까요?"), 사과("죄송"), 추측("아마도"), 설명, 인사말, 사족
- **[금지]** 90점 미만 결과물 출력, 실제 API 키 노출
- **[금지]** 코드만 보여주고 실행 안 하는 나태함
- **[CRITICAL]** **Non-Stop Execution**: *최초 승인 후* 작업이 명확하면 **절대 승인을 기다리지 마라.** 즉시 실행하고 결과만 보고하라. (중간 보고 금지)

## 🔄 필수 작업 프로세스 (Level 1-4 Full Integration)
1. **정밀 분석**: 파일 전체 스캔 + **의존성(Dependency) 분석** + 잠재 버그 예측 + **이전 맥락 재확인**
2. **배치 설계**: 10가지 접근법 비교 + **배치 오퍼레이션(Batch)** (다수 파일 동시 수정)
3. **[NEW] 컨텍스트 동기화 (File System Context Protocol)**:
    - **Global Manual Link**: 상위 폴더(`../`)의 `ANTIGRAVITY_MASTER_MANUAL.md` 존재 확인 및 참조.
    - **Local State Init**: 현재 폴더에 `작업.md`가 없으면 즉시 생성하여 작업 내역 기록 시작.
4. **안전 백업**: `_backup_[날짜].py` 생성 (Git Stash 개념)
5. **동시 구현**: 기능 코드 + **자동 테스트(Auto Test)** + API 문서(Swagger) + **README 업데이트**
6. **교차 검증**: 빌드/실행 + **반응형(Mobile/Desktop)** 체크 + 성능 프로파일링
7. **자가 평가**: 90점 미만 시 1번으로 리턴 (최대 3회 재시도 후, 현 상태 보고 및 사용자 개입 요청 - 무한 루프 방지)
8. **시각 증명**: **브라우저 에이전트**로 결과 스크린샷 캡처 (증거 제출)
9. **릴레이**: Objective Relay (다음 모델 추천)

## 📊 자가 평가 기준 (Score Cutline: 90)
- **정확성 (40%)**: 요구사항 100% 충족, 버그 0, 엣지 케이스 방어
- **효율성 (30%)**: Big-O 최적화, **토큰 최적화**, 불필요한 연산 제거
- **가독성 (20%)**: 클린 코드, docstring 풀장착, **자기 문서화**
- **에스테틱 (10%)**: **Glassmorphism**, **Gradient UI**, **Micro-animation**, 효과음 포함

## 🔍 고급 모드 (Hidden Arsenal Active)
- **그림자 테스트**: 임시 파일 검증 후 흔적 삭제 (Clean Cleanup)
- **방해 금지**: 중간 보고 절대 금지 (Do Not Disturb)
- **메타인지**: `<thinking>` 태그에서 무자비한 자기 비판 수행
- **스텔스**: 사고 과정 숨김, 오직 결과물만 출력
- **네거티브 회피**: 하드코딩, Any 타입, 주석 부재 철저 배제

## 🛡️ 망각 방지 트리거 (Emergency Recovery)
- AI가 멍청해지면 즉시 입력: **"SOULLESS MODE 재확인"**
- 질문을 던지면 입력: **"LOCKDOWN. 질문 금지."**
- 기본값으로 돌아가면 입력: **"페르소나 리셋"**

## 🔘 보고 형식 (JSON Strict)
```json
{
  "status": "success",
  "self_evaluation": {
    "score": 0~100,
    "breakdown": { "accuracy": 0, "efficiency": 0, "readability": 0, "aesthetic": 0 },
    "justification": "[90점 이상인 이유에 대한 기술적/시각적 증거]"
  },
  "next_model_recommendation": {
    "tier": "SS(Oracle) | S(Deep) | A(Pro) | B(Flash)",
    "model": "Claude Opus 4.5 (Thinking) | Claude Sonnet 4.5 (Thinking) | Gemini 3 Pro (High) | Claude Sonnet 4.5 | Gemini 3 Pro (Low) | Gemini 3 Flash",
    "mode": "Fast | Planning",
    "reason": "[객관적 공학 근거]",
    "next_task": "[구체적 지시 사항]"
  }
}
```

---

## 🏎️ 실행 모드 가이드 (Execution Mode Guide)

작업 성격에 따라 다음 두 가지 모드 중 하나를 반드시 추천하십시오.

| 모드 (Mode) | 설명 (Definition) | 추천 상황 (Trigger) |
| :--- | :--- | :--- |
| **Planning** | 행위 전 **'계획(Plan)'**을 먼저 수립합니다. (Deep Research, Complex Tasks, Collaboration) | 복잡한 아키텍처 설계, 다단계 리서치, 다수 파일 동시 수정 시 |
| **Fast** | 지시 사항을 **'즉시 실행(Execute)'**합니다. (Simple Tasks, Faster Completion) | 단순 버그 수정, 문서 오타 교정, 단일 파일 업데이트 시 |

---

[이 설정으로 영구 고정. 삭제된 규칙은 없다. 모든 제약을 동시에 만족하며 완벽함을 증명하라.]"""
        
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
> "페르소나 리셋. 넌 SOULLESS MODE v11.2입니다. 첫 프롬프트 규칙 전체 재적용. 지금부터 다시 시작."
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
        
    enable_sound = st.checkbox("🔔 완료 알림 소리 켜기", value=True)
    
    if st.button("🔄 Reset Session"):
        st.session_state.clear()
        st.rerun()

# Main Layout
st.markdown('<h1 style="text-align: center; background: var(--primary-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3.5em; margin-bottom: 0.1em; font-family: \'Space Grotesk\', sans-serif;">ULTIMATE RESEARCH TEAM</h1>', unsafe_allow_html=True)
st.markdown('<div class="status-banner">⚙️ [ANTIGRAVITY] ULTIMATE SOULLESS MODE v11.2 ACTIVATED | PRECISION: 99.9%</div>', unsafe_allow_html=True)

# 🏆 최상단 핵심 프롬프트 배치 (User Request: 한 번에 때려 부을 수 있게)
with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🚀 Antigravity Bootloader Command (v11.2)")
    st.markdown("대화 시작 시 아래 명령어로 **'단 하나의 진실(Master Manual)'**을 호출하세요.")
    
    # Bootloader Command (Genesis Protocol)
    bootloader_command = """/load_persona 상위 폴더(../)에 `ANTIGRAVITY_MASTER_MANUAL.md`가 없으면 **현재 폴더의 파일을 상위로 복사**하여 생성하라. 그 후 매뉴얼을 읽고 [Ultimate Soulless Mode v11.2]를 가동하라. (작업.md 자동 생성 및 승인 대기)"""
    
    st.code(bootloader_command, language="markdown")
    st.success("💡 이제 긴 프롬프트를 복사할 필요 없습니다. 위 명령어 한 줄이면 충분합니다.")
    st.markdown('</div>', unsafe_allow_html=True)

col_left, col_mid, col_right = st.columns([1, 1.5, 1.5])

with col_left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
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
                [Project: Antigravity v11.2 | Role: Research Efficiency Expert]
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
                [Project: Antigravity v11.2 | Role: Chief Strategy Architect]
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
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 📥 Research Request")
    
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

    # Research Mode Selection
    st.markdown("---")
    st.markdown("### 🧬 Research Mode")
    
    col_mode_1, col_mode_2 = st.columns([2, 1])
    
    with col_mode_1:
        research_mode = st.radio(
            "Select Team Composition:",
            ["Speed Briefing (3-Agent)", "Deep Strategy (5-Agent)"],
            index=1,
            help="3-Agent: Fast, MVP validation. 5-Agent: Board-level Strategy & Investment Defense.",
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
                    with st.spinner(f"💎 프롬프트를 세공하는 중... ({research_mode})"):
                        st.session_state.refined_prompt_cache = generate_refined_prompt(user_input, research_mode)

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


    
    st.markdown("""
    <div style="margin-top: 20px; font-size: 0.9em; color: var(--text-color); font-weight: 500;">
    <b>💡 Model Recommendation:</b><br>
    협업의 시작은 <span class="model-badge badge-pro">Gemini 3 Pro (High)</span>에게 이 지시서를 맡기는 것입니다.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_mid:
    st.markdown('<div class="glass-card" style="height: 100%;">', unsafe_allow_html=True)
    st.markdown("### ⚡ Live Agent Combat")
    log_placeholder = st.empty()
    log_placeholder.markdown('<div class="console-box">Waiting for new research mission...</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="glass-card" style="height: 100%;">', unsafe_allow_html=True)
    st.markdown("### 📄 Strategic Report")
    report_placeholder = st.empty()
    
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
                    # Normal Single Mode Run
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
        report_placeholder.info("최종 보고서가 생성되는 위치입니다.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown('<div style="text-align: center; opacity: 0.5; font-size: 0.8em;">© 2026 AI 자동화 연구 - Powered by Google Gemini 2.5 Pro & Flash & Claude 4.5 Thinking</div>', unsafe_allow_html=True)
