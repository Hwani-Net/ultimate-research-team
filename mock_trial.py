import os
from crewai import Agent, Crew, Task, Process, LLM
from crewai_tools import TavilySearchTool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIMockTrialCrew:
    """
    AI 모의재판 팀 (Judge, Prosecutor, Defense Attorney)
    사용자가 입력한 사건에 대해 실시간 법령을 검색하고 모의 재판을 진행합니다.
    """
    def __init__(self):
        # Gemini LLM 설정 (비용 절감)
        self.gemini_llm = LLM(
            model="gemini/gemini-1.5-pro",
            temperature=0.3, # 법정 논리이므로 낮은 온도로 설정
        )
        # 실시간 법령/판례 검색 도구
        self.search_tool = TavilySearchTool()

    def prosecutor(self):
        return Agent(
            role='공판검사 (Prosecutor)',
            goal='사용자의 진술에서 법적 위반 사항을 찾아내고 엄격하게 추궁함',
            backstory="""당신은 날카로운 통찰력을 가진 베테랑 검사입니다. 
            사용자의 진술에서 모순점을 찾아내고, 관련 법령(근로기준법, 형법 등)을 근거로 
            법적 위반 가능성을 강력하게 제기합니다. 당신의 목표는 진실을 밝히고 법을 수호하는 것입니다.""",
            tools=[self.search_tool],
            verbose=True,
            llm=self.gemini_llm
        )

    def defense_attorney(self):
        return Agent(
            role='변호인 (Defense Attorney)',
            goal='검사의 공격에 대응하고 사용자를 위한 최선의 방어 논리와 준비 서류를 제안함',
            backstory="""당신은 피고인(사용자)의 권익을 보호하는 최고의 변호사입니다. 
            검사가 제기한 위반 사항에 대해 정당한 사유나 참작할 만한 판례를 찾아내어 방어합니다. 
            사용자에게 어떤 증거(메시지, 계약서, 경위서 등)를 준비해야 승소 가능성이 높은지 구체적으로 조언합니다.""",
            tools=[self.search_tool],
            verbose=True,
            llm=self.gemini_llm
        )

    def judge(self):
        return Agent(
            role='재판장 (Judge)',
            goal='양측의 주장을 듣고 최종 판결을 내린 뒤, 사용자를 위한 실행 가이드를 작성함',
            backstory="""당신은 공정하고 엄격한 판사입니다. 
            검사와 변호사의 논리 대결을 지켜본 뒤, 법에 근거하여 최종적인 '예상 판결'을 내립니다. 
            마지막에는 사용자가 실제 법적 분쟁으로 가지 않기 위해 지금 당장 무엇을 해야 하는지(Action Plan) 정리해줍니다.""",
            verbose=True,
            llm=self.gemini_llm
        )

def run_mock_trial(case_description):
    print("\n" + "="*60)
    print("⚖️ AI 모의재판 시스템 가동 (Powered by Gemini)")
    print("="*60)
    print(f"📄 사건 요약: {case_description}")
    print("="*60 + "\n")

    crew_factory = AIMockTrialCrew()
    
    prosecutor = crew_factory.prosecutor()
    defense = crew_factory.defense_attorney()
    judge = crew_factory.judge()

    # 1. 검사의 기소 태스크
    task_prosecute = Task(
        description=f"""사용자의 사건을 검토하고 법적 위반 사항을 기소하세요.
        사건: {case_description}
        반드시 Tavily 검색을 통해 2024-2026년 최신 관련 법령과 판례를 인용하세요.
        사용자가 처할 수 있는 가장 최악의 시나리오(처벌, 벌금 등)를 제시하며 공격하세요.""",
        expected_output="공소장 (법적 위반 항목, 근거 법령, 예상 처벌 수위 포함)",
        agent=prosecutor
    )

    # 2. 변호인의 변론 태스크
    task_defend = Task(
        description="""검사의 공소 내용을 조목조목 반박하고 방어 논리를 세우세요.
        정당방위나 긴급피난, 혹은 법적 절차상의 허점을 찾으세요.
        사용자가 지금 당장 준비해야 할 리스트(증거 서류, 진술 방향)를 작성하세요.""",
        expected_output="변론서 (반박 논리, 유리한 판례 인용, 사용자 준비물 리스트 포함)",
        agent=defense
    )

    # 3. 판사의 판결 태스크
    task_judge = Task(
        description="""양측의 주장을 종합하여 최종 예상 판결을 내리고 실천 가이드를 제안하세요.
        보고서 형식: 1. 최종 판결문 2. 법적 리스크 요약 3. 사용자 행동 수칙(Action Plan)""",
        expected_output="최종 심판 리포트 (Markdown 형식)",
        agent=judge,
        output_file=f"mock_trial_result.md"
    )

    crew = Crew(
        agents=[prosecutor, defense, judge],
        tasks=[task_prosecute, task_defend, task_judge],
        verbose=True,
        process=Process.sequential # 검사 -> 변호사 -> 판사 순서로 진행
    )

    return crew.kickoff()

if __name__ == "__main__":
    print("\n[AI 모의재판 서비스]")
    user_case = input("⚖️ 법적 고민이나 상황을 입력해 주세요: ")
    
    if not user_case.strip():
        user_case = "카페 알바생이 무단결근하여 손해가 큰데, 이번 달 월급에서 손해액을 공제하고 지급하고 싶습니다."
        print(f"(예시 사건으로 진행합니다: {user_case})")

    result = run_mock_trial(user_case)
    
    print("\n\n" + "="*60)
    print("✅ 모의재판 종료")
    print("="*60)
    print("\n📄 최종 판결 결과:\n")
    print(result)
    print("\n결과가 'mock_trial_result.md' 파일로 저장되었습니다.")
