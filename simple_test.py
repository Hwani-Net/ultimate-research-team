import os
from dotenv import load_dotenv
from crewai import Agent, Crew, Task, Process
from crewai_tools import TavilySearchTool

# Load environment variables
load_dotenv()

# Simple test without complex LLM configuration
def simple_test():
    """Simplified test using default OpenAI"""
    
    print("=" * 60)
    print("🧪 SIMPLIFIED TEST - Using OpenAI GPT-4")
    print("=" * 60)
    print("📋 Topic: Gemini의 최신 버전과 가격 정보")
    print("🔍 Search: Tavily AI")
    print("=" * 60)
    
    # Check API keys
    if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "sk-dummy-key-not-used":
        print("\n❌ Error: Valid OPENAI_API_KEY required")
        print("   Please add your OpenAI API key to .env file")
        print("   Or we can use Gemini directly via Google AI SDK")
        return
    
    if not os.getenv("TAVILY_API_KEY"):
        print("\n❌ Error: TAVILY_API_KEY required")
        return
    
    try:
        # Create search tool
        search_tool = TavilySearchTool()
        
        # Create a simple researcher agent (using default OpenAI)
        researcher = Agent(
            role='Real-Time Information Specialist',
            goal='Search for the LATEST information about Gemini models and pricing',
            backstory="""You are an expert researcher who always searches the web for current information.
            Focus on finding the most recent Gemini model versions and their pricing.""",
            tools=[search_tool],
            verbose=True,
        )
        
        # Create task
        task = Task(
            description="""Search the web for:
            1. Latest Gemini model versions (check if Gemini 3.0 exists)
            2. Current pricing for Gemini models
            3. Publication dates of your sources
            
            Focus on sources from 2024-2026.""",
            expected_output="A brief report with latest Gemini versions, pricing, and source dates",
            agent=researcher,
        )
        
        # Create crew
        crew = Crew(
            agents=[researcher],
            tasks=[task],
            verbose=True,
            process=Process.sequential,
        )
        
        print("\n🔄 Starting research...")
        print("=" * 60)
        result = crew.kickoff()
        
        print("\n\n" + "=" * 60)
        print("✅ RESEARCH COMPLETE!")
        print("=" * 60)
        print("\n📄 Result:\n")
        print(result)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    simple_test()
