"use client";

import { useState } from "react";

export default function Home() {
  const [role, setRole] = useState("");
  const [questions, setQuestions] = useState([]);
  const [selectedQuestion, setSelectedQuestion] = useState(null);
  const [answer, setAnswer] = useState("");
  const [feedback, setFeedback] = useState("");
  const [loading, setLoading] = useState(false);
  const [feedbackLoading, setFeedbackLoading] = useState(false);
  const [error, setError] = useState("");

  // 질문 불러오기
  const handleFetchQuestions = async () => {
    if (!role.trim()) {
      setError("직무를 입력해주세요.");
      return;
    }
    setError("");
    setLoading(true);
    setQuestions([]);
    setFeedback("");
    setSelectedQuestion(null);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/questions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          user_role: role, // ? Flask가 요구하는 필드명
          seniority: "주니어",
          num_questions: 5,
          language: "ko",  }),
      });

      const data = await res.json();

      if (res.ok && data.questions) {
        setQuestions(data.questions);
      } else {
        setError(data.error || "질문을 불러오지 못했습니다.");
      }
    } catch (err) {
      setError("서버에 연결할 수 없습니다.");
    } finally {
      setLoading(false);
    }
  };

  // 피드백 받기
  const handleGetFeedback = async () => {
    if (!selectedQuestion || !answer.trim()) {
      setError("답변을 입력해주세요.");
      return;
    }
    setError("");
    setFeedback("");
    setFeedbackLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          role,
          question: selectedQuestion,
          answer,
        }),
      });

      const data = await res.json();
      if (res.ok && data.feedback) {
        setFeedback(data.feedback);
      } else {
        setError(data.error || "피드백 생성 실패");
      }
    } catch (err) {
      setError("서버 요청 중 오류가 발생했습니다.");
    } finally {
      setFeedbackLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-6 bg-gray-50">
      <div className="max-w-2xl w-full bg-white p-8 rounded-2xl shadow-lg">
        <h1 className="text-2xl font-bold text-center mb-6">
          ? 직무 기반 면접 연습 도우미
        </h1>

        {/* 직무 입력 */}
        <div className="flex gap-2 mb-4">
          <input
            type="text"
            placeholder="예: 백엔드 개발자, 데이터 분석가..."
            value={role}
            onChange={(e) => setRole(e.target.value)}
            className="flex-1 border rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-400 outline-none"
          />
          <button
            onClick={handleFetchQuestions}
            disabled={loading}
            className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 disabled:bg-blue-300"
          >
            {loading ? "생성 중..." : "질문 생성"}
          </button>
        </div>

        {/* 에러 메시지 */}
        {error && (
          <p className="text-red-500 text-sm mb-4 text-center">{error}</p>
        )}

        {/* 질문 목록 */}
        {questions.length > 0 && (
          <div className="mt-4">
            <h2 className="text-lg font-semibold mb-2 text-gray-700">
              {role} 면접 질문 목록
            </h2>
            <ul className="space-y-2">
              {questions.map((q, idx) => (
                <li
                  key={idx}
                  onClick={() => {
                    setSelectedQuestion(q);
                    setFeedback("");
                    setAnswer("");
                  }}
                  className={`border rounded-lg p-3 cursor-pointer transition ${
                    selectedQuestion === q
                      ? "bg-blue-100 border-blue-400"
                      : "bg-gray-100 hover:bg-gray-200"
                  }`}
                >
                  {idx + 1}. {q}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* 선택된 질문 및 답변 입력 */}
        {selectedQuestion && (
          <div className="mt-6 border-t pt-4">
            <h3 className="text-md font-semibold mb-2 text-gray-800">
              선택된 질문:
            </h3>
            <p className="bg-gray-50 p-3 rounded-lg mb-3">{selectedQuestion}</p>

            <textarea
              placeholder="이 질문에 대한 나의 답변을 입력해보세요..."
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              className="w-full h-32 border rounded-lg p-3 focus:ring-2 focus:ring-blue-400 outline-none resize-none"
            ></textarea>

            <button
              onClick={handleGetFeedback}
              disabled={feedbackLoading}
              className="mt-3 bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 disabled:bg-green-300"
            >
              {feedbackLoading ? "피드백 생성 중..." : "피드백 받기"}
            </button>

            {/* 피드백 결과 */}
            {feedback && (
              <div className="mt-4 p-4 border rounded-lg bg-green-50 text-gray-800 whitespace-pre-line">
                <h4 className="font-semibold mb-2">? 면접관 피드백</h4>
                {feedback}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
