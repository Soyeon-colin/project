# -*- coding: utf-8 -*-

import os
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from difflib import get_close_matches

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI

# 0) 환경 설정
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 1) 직무 프로파일 정의

# 2) 사용자 입력 직무 정규화

# 4) 질문 생성 로직
# def get_questions_for_role(
    
# 5) Flask 앱
app = Flask(__name__)
CORS(app)  # 필요 시 도메인 지정: CORS(app, resources={r"/api/*": {"origins": "https://your-frontend"}})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/generate_questions", method = ["POST"])
def generate_questions():
    """
    요청(JSON):
    {
        "job_position": "데이터 분석가"
    }

    응답(JSON):
    {
        "questions": [
            {"question": "이 직무를 선택한 이유는 무엇인가요?"},
            {"question": "데이터 분석 과정에서 가장 중요한 단계는 무엇이라고 생각하나요?"},
            ...
        ]
    }
    """
    data = request.get_json(silent=True) or {}
    job = (data.get("job_position") or "").strip()

    if not job:
        return jsonify({"error": "직무(job_position)는 필수 입력 항목입니다."}), 400

    #프롬프트 구성
    prompt = f"""
당신은 면접관입니다. 사용자가 지원하는 직무에 맞추어 실제 면접에서 사용할 질문 5개를 생성하세요.
각 질문은 명확하고 실무 중심이어야 하며, 불필요한 팁이나 설명은 포함하지 마세요.

출력 형식은 아래 JSON 구조를 따르세요:
{{
  "questions": [
    {{"question": "질문 1"}},
    {{"question": "질문 2"}},
    {{"question": "질문 3"}},
    {{"question": "질문 4"}},
    {{"question": "질문 5"}}
  ]
}}

지원 직무: {job}
"""

    try:
        #OpenAI API 호출
        resp = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {"role": "system", "content": "당신은 전문 면접관입니다. 사용자의 직무에 맞는 질문을 구성합니다."},
                {"role": "user", "content": prompt}
            ]
        )

        raw = resp.choices[0].message.content

        #모델의 JSON 파싱 시도
        try:
            parsed = json.loads(raw)
            if not isinstance(parsed, dict) or "questions" not in parsed:
                raise ValueError("questions 키가 없습니다.")
            return jsonify(parsed), 200
        except Exception:
            #JSON 파싱 실패 시 원문 반환
            return jsonify({
                "warning": "모델 응답을 JSON으로 파싱하지 못했습니다. raw 필드를 확인하세요.",
                "raw": raw
            }), 200

    except Exception as e:
        return jsonify({"error": f"OpenAI 호출 실패: {e}"}), 500


# @app.route("/api/feedback", methods=["POST"])
# def api_feedback():
#     try:
#         data = request.get_json(force=True)
#         question = data.get("question")
#         answer = data.get("answer")
#         role = data.get("role", "IT/백엔드")

#         if not question or not answer:
#             return jsonify({"error": "question and answer are required"}), 400

#         prompt = f"""
#             당신은 {role} 직무의 면접관입니다.
#             아래는 지원자의 답변입니다. 피드백을 구체적으로 작성해주세요.

#             질문: {question}
#             답변: {answer}

#             평가 기준:
#             - 논리적 구조
#             - 전달력
#             - 창의성
#             - 표현력
#             - 실무 적합성
#             - 개선 포인트
#                     """

#         resp = client.responses.create(
#             model="gpt-",
#             input=prompt,
#             temperature=0.5,
#             max_output_tokens=400
#         )

#         feedback = resp.output_text
#         return jsonify({"feedback": feedback})

#     except Exception as e:
#         return jsonify({"error": "feedback_generation_failed", "detail": str(e)}), 500


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    port = int(os.getenv("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=True)