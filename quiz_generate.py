import os
import json
from flask import Flask, request, jsonify
from openai import OpenAI

from services.ai_engine import generate_quiz_from_resume


app = Flask(__name__)

# -------------------------
# 환경 변수 로드
# -------------------------
load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise EnvironmentError("OPENAI_API_KEY 누락됨 (.env 확인)")

client = OpenAI(api_key=API_KEY)

@app.route('/api/generate-quiz', methods=['POST'])
def get_quiz():
    data = request.json
    resume_text = data.get('resume')
    job_role = data.get('job_role')


    prompt =
    f"""사용자가 입력한 자소서{resume_text}를 분석하여 {job_role} 기반의 퀴즈를 생성하시오

    자소서 분석 시 다음 항목을 중점적으로 고려하시오:
    ● 역량 태깅: 자소서 문장에서 [데이터 분석], [협업], [문제 해결], [리더십] 등의 키워드를 
    추출합니다. 
    ● 팩트 추출: '매출 20% 상승', '3개월간 진행', '5명의 팀원' 등 수치와 고유 명사를 따로 
    저장합니다. 
    ● 논리 망(Logic Net) 구축: 문제 상황 -> 해결책 -> 결과의 연결 고리가 단단한지 
    점검합니다.
    
    분석된 재료를 바탕으로 퀴즈는 다음 형식을 따르시오:
      
      ● 유형 A (진위 확인): 자소서의 팩트를 교묘하게 비튼 질문 (예: "본인이 기여한 핵심 기술이 
      A라고 했는데, 실제 결과물 B와 어떤 상관관계가 있나요?") 
      ● 유형 B (직무 매칭): "이 에피소드를 전략 기획 직무 면접에서 말한다면, 어떤 역량을 가장 
      강조하는 것이 유리할까요?" 
      ● 유형 C (꼬리 질문): 답변 후 예상되는 '압박 꼬리 질문'을 생성합니다. 
    
      질문 수준 선택은 다음과 같습니다:
      ● 초급(신입): 기본적인 이해도를 평가하는 질문
      ● 중급(주니어): 직무 관련 상황 판단 능력을 묻는 질문
      ● 고급(시니어): 심층적 사고와 문제 해결 능력을 요구하는 질문
    
    퀴즈 출력 형식은 JSON으로 다음과 같이 구성하시오:

    [
       질문은 모범답변(객관식) 선택 4문제, 위기대응형(주관식) 문제 2문제
        {
        
  "quiz_set": [
    {
      "id": "Q1",
      "type": "유형 A (진위 확인)",
      "difficulty": "중급",
      "question": "자소서에서 프로젝트 A의 성과를 20% 개선했다고 기술하셨습니다. 만약 면접관이 '해당 수치가 시장의 자연 성장분인지 본인의 기여인지'를 묻는다면 가장 적절한 답변 전략은 무엇입니까?",
      "options": [
        "1. 시장 상황 덕분이었다고 솔직하게 말한다.",
        "2. 팀 전체의 성과이므로 개인의 기여도를 나누기 어렵다고 답한다.",
        "3. 본인이 도입한 구체적 방법론(A)과 그에 따른 수치 변화를 대조하여 입증한다.",
        "4. 수치보다는 협업 과정에서의 배운 점을 강조하며 화제를 전환한다."
      ],
      "explanation": "유형 A는 팩트의 논리적 근거를 묻습니다. 성과와 행동 사이의 명확한 상관관계를 입증하는 3번이 직무 특화 답변입니다.",
      "tags": ["문제 해결", "데이터 기반 사고"]
    },
    {
      "id": "Q5",
      "type": "유형 C (위기 대응)",
      "difficulty": "고급",
      "question": "프로젝트 기간이 3개월로 다소 짧아 보이는데, 이 기간 내에 심도 있는 분석이 가능했나요? (약점 보완 질문)",
      "defense_keywords": ["사전 조사", "효율적 리소스 배분", "핵심 지표 집중"],
      "answer_guide": "입력창: [사전 조사]를 통해 시행착오를 줄이고, [핵심 지표 집중] 전략으로 단기간 내 성과를 도출했습니다."
    }
  ]
} 

      """
