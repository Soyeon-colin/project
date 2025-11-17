"use client";

import { useState } from "react";

export default function Home() {
  const [job, setJob] = useState("");
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // 질문 생성 요청
  const handleGenerateQuestions = async () => {
    if (!job.trim()) {
      setError("직무를 입력해주세요.");
      return;
    }

    setError("");
    setLoading(true);
    setQuestions([]);

    try {
      const res = await fetch("http://127.0.0.1:5000/generate_questions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ job_position: job }),
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

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-6 bg-gray-50">
      <div className="max-w-2xl w-full bg-white p-8 rounded-2xl shadow-lg">
        <h1 className="text-2xl font-bold text-center mb-6">
          💼 직무 기반 면접 질문 생성기
        </h1>

        {/* 직무 입력 */}
        <div className="flex gap-2 mb-4">
          <input
            type="text"
            placeholder="예: 데이터 분석가, 프론트엔드 개발자..."
            value={job}
            onChange={(e) => setJob(e.target.value)}
            className="flex-1 border rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-400 outline-none"
          />
          <button
            onClick={handleGenerateQuestions}
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

        {/* 질문 리스트 */}
        {questions.length > 0 && (
          <div className="mt-6">
            <h2 className="text-lg font-semibold mb-3 text-gray-700">
              생성된 질문
            </h2>
            <ul className="space-y-3">
              {questions.map((q, idx) => (
                <li key={idx} className="border p-3 rounded-lg bg-gray-100">
                  <strong>{idx + 1}. </strong> {q.question}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
