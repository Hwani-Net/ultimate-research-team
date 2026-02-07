import os
from crewai import Crew, Process
from agents import UltimateResearchAgents
from tasks import UltimateResearchTasks
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_gemini_setup_research():
    """
    Research strictly how to use CrewAI with Gemini ONLY (No OpenAI dependency)
    """
    # 1. Define the specific research topic (Pre-defined to avoid input errors)
    topic = "Google Gemini for CrewAI without OpenAI"
    
    research_prompt = """
    CrewAI 프레임워크를 사용하여 AI 에이전트 팀을 운영하려고 하는데, 
    OpenAI API를 전혀 사용하지 않고 오직 "Google Gemini" (Gemini 2.0/3.0) API만 사용하는 
    구체적인 파이썬 코드 설정 방법을 조사해줘.

    다음 사항들을 반드시 조사하고 포함해:
    1. 라이브러리 의존성: `langchain-google-genai` 설치 필요 여부 및 `crewai[tools]` 호환성.
    2. 정확한 모델 문자열: 2026년 기준 CrewAI에서 작동하는 Gemini 모델 ID 
       (예: `gemini/gemini-pro`, `gemini/gemini-1.5-pro` 등).
    3. "OPENAI_API_KEY Missing" 오류 우회법: 
       - 왜 Gemini를 쓰는데도 OpenAI 키를 요구하는지 원인 분석
       - `.env`에 더미 키(`sk-proj-dummy...`)를 넣으면 해결되는지 확인
    4. 코드 예시: 
       - `LLM(model="gemini/...")` 방식이 맞는지
       - `ChatGoogleGenerativeAI` 클래스를 직접 사용하는 것이 더 안정적인지 비교
    
    목표: "비용 0원"으로 CrewAI를 돌리는 완벽한 `agents.py` 설정 가이드를 작성해줘.
    """
    
    print("=" * 60)
    print("🧠 GEMINI SETUP RESEARCHER")
    print("=" * 60)
    print(f"🎯 Objective: Find how to remove OpenAI dependency and use proper Gemini config")
    print("=" * 60)
    
    # 2. Instantiate Agents
    agents = UltimateResearchAgents()
    researcher = agents.deep_researcher()
    critic = agents.critical_analyst()
    writer = agents.insight_synthesizer()

    # 3. Instantiate Tasks
    tasks = UltimateResearchTasks()
    
    # Customizing tasks for this specific technical research
    task1 = tasks.initial_research_task(researcher, research_prompt)
    task2 = tasks.critical_review_task(critic)
    task3 = tasks.refinement_research_task(researcher)
    
    # Overriding the final task to force a safe filename
    task4 = tasks.final_report_task(writer, research_prompt)
    task4.output_file = "gemini_setup_guide.md"  # <--- FIX: Safe short filename
    
    # 4. Create Crew
    crew = Crew(
        agents=[researcher, critic, writer],
        tasks=[task1, task2, task3, task4],
        verbose=True,
        process=Process.sequential,
        memory=True,
    )
    
    print("\n🚀 Starting research (this will take 2-3 minutes)...")
    result = crew.kickoff()
    return result

if __name__ == "__main__":
    run_gemini_setup_research()
