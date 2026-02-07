import os
import sys
from crewai import Crew, Process
from agents import UltimateResearchAgents
from tasks import UltimateResearchTasks
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_team():
    """Quick test of the research team"""
    topic = "Gemini의 최신 버전과 가격 정보"
    
    print("=" * 60)
    print("🧪 TESTING ULTIMATE RESEARCH TEAM")
    print("=" * 60)
    print(f"📋 Topic: {topic}")
    print(f"🤖 Models: Gemini 3.0 Flash + Pro")
    print(f"🔍 Search: Tavily AI")
    print("=" * 60)
    
    try:
        # 1. Create agents
        print("\n1️⃣ Creating agents...")
        agents = UltimateResearchAgents()
        researcher = agents.deep_researcher()
        critic = agents.critical_analyst()
        writer = agents.insight_synthesizer()
        print("   ✅ Agents created")
        
        # 2. Create tasks
        print("\n2️⃣ Creating tasks...")
        tasks = UltimateResearchTasks()
        task_research = tasks.initial_research_task(researcher, topic)
        task_critique = tasks.critical_review_task(critic)
        task_refine = tasks.refinement_research_task(researcher)
        task_write = tasks.final_report_task(writer, topic)
        print("   ✅ Tasks created")
        
        # 3. Create crew
        print("\n3️⃣ Creating crew...")
        crew = Crew(
            agents=[researcher, critic, writer],
            tasks=[task_research, task_critique, task_refine, task_write],
            verbose=True,
            process=Process.sequential,
            memory=True,
            planning=True,
        )
        print("   ✅ Crew created")
        
        # 4. Execute
        print("\n4️⃣ Starting research (this may take 2-3 minutes)...")
        print("=" * 60)
        result = crew.kickoff()
        
        print("\n\n" + "=" * 60)
        print("✅ RESEARCH COMPLETE!")
        print("=" * 60)
        print("\n📄 Final Report:\n")
        print(result)
        
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_team()
