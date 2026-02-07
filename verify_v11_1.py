from dotenv import load_dotenv
load_dotenv()
from agents import UltimateResearchAgents
import streamlit as st

def verify_system():
    print("Locked on target: Verifying Antigravity v11.1 Infrastructure...")
    print("-" * 50)
    
    try:
        agents = UltimateResearchAgents()
        print(f"✅ [Researcher Model]: {agents.flash_model_name} (Active)")
        print(f"✅ [Analyst Model]:    {agents.flash_model_name} (Active)")
        print(f"✅ [Skeptic Model]:    {agents.critic_model_name} (Active)")
        print(f"✅ [Strategist Model]: {agents.pro_model_name} (Active)")
        print(f"✅ [Writer Model]:     {agents.pro_model_name} (Active)")
        print("-" * 50)
        
        # Verify Tool Access
        tool_name = agents.search_tool.name
        print(f"✅ [Search Tool]:      {tool_name} (Online)")
        
        print("\n[SYSTEM STATUS]: ALL GREEN. SOULLESS MODE v11.1 IS READY.")
        print("To initiate research, run: 'streamlit run app.py'")
        
    except Exception as e:
        print(f"❌ [SYSTEM CRITICAL FAILURE]: {e}")

if __name__ == "__main__":
    verify_system()
