import os
from crewai import Crew, Process
from agents import UltimateResearchAgents
from tasks import UltimateResearchTasks
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_ultimate_team(topic):
    """
    Execute the Ultimate Research Team with Gemini 3.0 models
    
    Architecture:
    - Flash model for fast information gathering
    - Pro model for deep analysis and writing
    - Sequential process with validation loop
    """
    print("=" * 60)
    print("🚀 ULTIMATE RESEARCH TEAM (Gemini 3.0)")
    print("=" * 60)
    print(f"📋 Topic: {topic}")
    print(f"🤖 Models: Gemini 3.0 Flash + Pro")
    print("=" * 60)
    
    # 1. Instantiate Agents (Gemini 3.0 powered)
    agents = UltimateResearchAgents()
    researcher = agents.deep_researcher()
    critic = agents.critical_analyst()
    writer = agents.insight_synthesizer()

    # 2. Instantiate Tasks
    tasks = UltimateResearchTasks()
    
    # Task Flow: Research → Critique → Refine → Write
    task_research = tasks.initial_research_task(researcher, topic)
    task_critique = tasks.critical_review_task(critic)
    task_refine = tasks.refinement_research_task(researcher)
    task_write = tasks.final_report_task(writer, topic)

    # 3. Create Crew with Sequential Process
    # This enforces the "Reflection Loop" pattern from Stanford research
    crew = Crew(
        agents=[researcher, critic, writer],
        tasks=[task_research, task_critique, task_refine, task_write],
        verbose=True,
        process=Process.sequential,  # Guarantees the debate/reflection flow
        memory=True,  # Shared memory for context
        planning=True,  # Enable planning capabilities
    )

    print("\n🔄 Starting the validation loop...")
    print("   Step 1: Deep Research (Flash model)")
    print("   Step 2: Critical Review (Pro model)")
    print("   Step 3: Targeted Refinement (Flash model)")
    print("   Step 4: Strategic Report (Pro model)")
    print("\n" + "=" * 60 + "\n")
    
    result = crew.kickoff()
    return result

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("   🧠 ULTIMATE RESEARCH TEAM - GEMINI 3.0 EDITION")
    print("=" * 60)
    print("\n💡 This team uses MIT/Stanford research patterns:")
    print("   • Multi-Agent Debate for accuracy")
    print("   • Reflection Loop for self-correction")
    print("   • Hierarchical task decomposition\n")
    
    user_topic = input("🔍 Enter your research topic: ")
    
    if not user_topic.strip():
        user_topic = "2026년 생성형 AI 시장 전망과 주요 트렌드"
        print(f"   (Using example topic: {user_topic})")
    
    result = run_ultimate_team(user_topic)
    
    print("\n\n" + "=" * 60)
    print("✅ RESEARCH COMPLETE")
    print("=" * 60)
    print("\n📄 Final Report:\n")
    print(result)
    print("\n" + "=" * 60)
    print("💾 Report saved to: final_report_*.md")
    print("=" * 60)
