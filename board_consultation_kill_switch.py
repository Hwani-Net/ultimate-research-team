import os
import sys
from crewai import Crew, Process, Task
from agents import BoardOfDirectors
from dotenv import load_dotenv

load_dotenv()
sys.stdout.reconfigure(encoding='utf-8')

# Consultation Question
consultation_topic = """
[STRATEGIC CONSULTATION REQUEST]

Topic: "Kill Switch Protocol - Role Definition"

Context:
We've implemented a "Kill Switch" that runs BEFORE the Board Meeting to detect fatal flaws.
Current Kill Switch checks:
1. Trademark conflicts (CLO)
2. Extreme red ocean saturation (Researcher)

Problem:
These checks OVERLAP with what the Board of Directors already does in their strategy session.

Question for the Board:
Should the Kill Switch be:

**Option A: Narrow Scope (Only Obvious Kills)**
- Only block projects that are 100% clearly doomed:
  * Illegal activities (drugs, weapons)
  * Identical trademark infringement (exact name match)
  * Zero TAM (literally no market)
- Let the Board handle everything else (similar trademarks, competitive markets, etc.)

**Option B: Current Scope (Maintained)**
- Keep checking trademark conflicts and red ocean
- Accept some overlap with Board duties
- Argument: Saves Board time by filtering out low-quality projects

**Option C: Expanded Scope**
- Add more checks (legal compliance, technical feasibility, economic viability)
- Turn Kill Switch into a comprehensive pre-screening
- Argument: Board only sees high-quality, pre-vetted proposals

Please debate this and provide:
1. Your individual perspectives (CEO, CFO, CTO, CMO, CLO)
2. Areas of agreement/disagreement
3. Final consensus recommendation
"""

def run_board_consultation():
    print("\n🏛️ [EMERGENCY BOARD CONSULTATION]")
    print("=" * 70)
    print("Topic: Kill Switch Protocol - Role Definition")
    print("-" * 70)
    
    board = BoardOfDirectors()
    
    # Assemble Board
    ceo = board.ceo()
    cfo = board.cfo()
    cto = board.cto()
    cmo = board.cmo()
    clo = board.clo()
    
    # Create consultation task
    consultation_task = Task(
        description=consultation_topic,
        expected_output="""A detailed board discussion transcript showing:
        1. Each member's perspective (with model name attribution)
        2. Points of agreement and disagreement
        3. Final consensus recommendation (Option A, B, or C)
        4. Rationale for the chosen option""",
        agent=ceo  # CEO chairs the meeting
    )
    
    board_crew = Crew(
        agents=[ceo, cfo, cto, cmo, clo],
        tasks=[consultation_task],
        verbose=True,
        process=Process.sequential,
        memory=False
    )
    
    print("\n🎯 Board deliberation in progress...\n")
    result = board_crew.kickoff()
    
    consultation_minutes = str(result)
    
    print("\n" + "=" * 70)
    print("📋 [BOARD CONSULTATION RESULT]")
    print("=" * 70)
    print(consultation_minutes)
    
    # Save result
    with open("kill_switch_board_decision.md", "w", encoding="utf-8") as f:
        f.write("# Board Consultation: Kill Switch Role Definition\n\n")
        f.write(consultation_minutes)
    
    print("\n✅ Consultation complete. Decision saved to 'kill_switch_board_decision.md'")

if __name__ == "__main__":
    run_board_consultation()
