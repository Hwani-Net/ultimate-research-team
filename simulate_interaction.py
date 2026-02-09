import os
import sys
import contextlib
from crewai import Crew, Process
from agents import BoardOfDirectors, ProjectTeam
from tasks import BoardTasks, ProjectTeamTasks
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Force standard output encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Mock Streamlit container for terminal output
class TerminalContainer:
    def markdown(self, text, unsafe_allow_html=False):
        # Remove HTML tags for terminal clarity
        clean_text = text.replace('<div class="console-box">', '').replace('</div>', '')
        print(clean_text)

def run_simulation(project_idea):
    """
    Simulates the interaction between Board of Directors and Project Team.
    """
    print(f"\n🚀 [SIMULATION START] Project: {project_idea}")
    print("=" * 70)
    
    # === PHASE 0: KILL SWITCH (PRE-BOARD SCREENING) ===
    print("\n🛡️ [PHASE 0] KILL SWITCH - PRE-BOARD SCREENING")
    print("-" * 70)
    
    board = BoardOfDirectors()
    from agents import UltimateResearchAgents  # Import research team
    research_team = UltimateResearchAgents()
    board_tasks = BoardTasks()
    
    # Get CLO and Deep Researcher for kill switch
    clo = board.clo()
    researcher = research_team.deep_researcher()
    
    # Run Kill Switch
    kill_switch_task = board_tasks.kill_switch_task(clo, researcher, project_idea)
    
    kill_switch_crew = Crew(
        agents=[clo, researcher],
        tasks=[kill_switch_task],
        verbose=True,
        process=Process.sequential,
        memory=False
    )
    
    print("\n🎯 Running Kill Switch Protocol...")
    kill_result = kill_switch_crew.kickoff()
    
    # Parse structured output (Handled similarly to app.py)
    if hasattr(kill_result, 'pydantic'):
        kill_data = kill_result.pydantic
    else:
        # Fallback for manual parsing if pydantic attribute missing
        import json
        from models import KillSwitchResult
        try:
            kill_data = KillSwitchResult.model_validate_json(kill_result.raw)
        except:
            print("⚠️ Failed to parse structured output. Falling back to string check.")
            kill_decision = str(kill_result)
            if "KILL" in kill_decision.upper():
                print(f"\n❌ [PROJECT TERMINATED]\nReason: String match 'KILL'\n{kill_decision}")
                return
            kill_data = None

    if kill_data:
        print("\n✅ [KILL SWITCH RESULT - STRUCTURED]")
        print("=" * 40)
        print(f"Decision: {kill_data.decision}")
        if kill_data.gate_failed:
            print(f"Gate Failed: #{kill_data.gate_failed} - {kill_data.gate_name}")
        print(f"Reason: {kill_data.reason}")
        print(f"Evidence: {kill_data.evidence or 'N/A'}")
        
        if kill_data.decision == "KILL":
            print("\n❌ [PROJECT TERMINATED]")
            print("The Kill Switch detected fatal flaws. Project will NOT proceed to Board.")
            return

    print("\n✅ Kill Switch: PASS. Proceeding to Board Meeting...")
    
    # === PHASE 1: BOARD STRATEGY SESSION ===
    print("\n🏛️ [PHASE 1] BOARD OF DIRECTORS MEETING")
    print("-" * 70)
    
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
    board_crew = Crew(
        agents=[ceo, cfo, cto, cmo, clo],
        tasks=[strategy_task],
        verbose=True,
        process=Process.sequential,
        memory=False
    )
    
    print("\n🎯 Board Strategy Session in progress...")
    board_result = board_crew.kickoff()
    
    # Handle result type
    board_minutes = str(board_result)
    
    print("\n✅ [BOARD DECISION]")
    print("=" * 30)
    print(board_minutes[:500] + "...\n(Full minutes omitted for brevity)")
    
    # Check for approval
    if "APPROVED" not in board_minutes.upper() and "GO" in board_minutes.upper():
        print("\n🎉 Project APPROVED by Board.")
        approved = True
    elif "REJECTED" in board_minutes.upper() or "NO-GO" in board_minutes.upper():
        print("\n🚫 Project REJECTED by Board.")
        return
    else:
        print("\n⚠️ Conditional Approval granted.")
        approved = True
        
    if not approved:
        return

    # === PHASE 2: PROJECT TEAM EXECUTION ===
    print("\n\n🔨 [PHASE 2] PROJECT TEAM HANDOVER")
    print("-" * 70)
    print("📢 PM: 'Board approved the plan. Team, let's get to work!'")
    
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
    
    planning_crew = Crew(
        agents=[pm],
        tasks=[planning_task],
        verbose=True,
        process=Process.sequential,
        memory=False
    )
    
    print("\n🎯 PM is breaking down the tasks...")
    planning_result = planning_crew.kickoff()
    implementation_plan = str(planning_result)
    
    print("\n✅ Implementation Plan Drafted.")
    
    # === PHASE 3: ARCHITECT SQUAD BLUEPRINT ===
    print("\n\n📐 [PHASE 3] ARCHITECT SQUAD BLUEPRINTING")
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
    
    print("\n🎯 Architects are generating technical specs...")
    blueprint_result = architect_crew.kickoff()
    final_blueprint = str(blueprint_result)
    
    print("\n✅ [BLUEPRINT GENERATED]")
    print(final_blueprint[:500] + "...")
    
    # Save for verification
    with open("simulation_blueprint.md", "w", encoding="utf-8") as f:
        f.write(final_blueprint)
    
    print("\n🎉 [SIMULATION COMPLETE] Interaction verified successfully.")

if __name__ == "__main__":
    # Test with EXACT trademark match to trigger Gate 2
    run_simulation("Notion")
