import { useEffect, useState } from "react";
import { Link, Navigate, useLocation, useNavigate } from "react-router-dom";
import { startAssessment, submitAssessment } from "../services/api";
import { DIFFICULTIES, LEVEL_NAMES } from "../lib";

export default function Assessment() {
  const { state } = useLocation();
  const navigate = useNavigate();
  const subject = state?.subject;
  const level = state?.level;

  const [session, setSession] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!subject || !level) return;
    let cancelled = false;
    startAssessment(subject.id, level)
      .then((d) => {
        if (cancelled) return;
        setSession(d.session_token);
        setQuestions(d.questions);
      })
      .catch((e) => !cancelled && setError(e.message))
      .finally(() => !cancelled && setLoading(false));
    return () => { cancelled = true; };
  }, [subject, level]);

  if (!subject || !level) return <Navigate to="/dashboard" replace />;

  const answered = Object.keys(answers).length;

  async function finish() {
    setError("");
    setSubmitting(true);
    try {
      const result = await submitAssessment(session, answers);
      navigate("/result", { state: { result, subject }, replace: true });
    } catch (e) {
      setError(e.message);
      setSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white p-8">
      <div className="max-w-4xl mx-auto">
        <Link to="/dashboard" className="text-slate-400 hover:text-white inline-block mb-6">← Back to Dashboard</Link>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 mb-8 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <p className="text-blue-400 font-semibold">Level {level}</p>
            <h1 className="text-4xl font-bold mt-1">{subject.name} Assessment</h1>
            <p className="text-slate-400 mt-2">{LEVEL_NAMES[level]} Level • {DIFFICULTIES[level]} Questions</p>
          </div>
          <div className="bg-slate-800 rounded-xl px-5 py-4 text-center">
            <p className="text-sm text-slate-400">Answered</p>
            <p className="text-2xl font-bold">{answered}/{questions.length || 10}</p>
          </div>
        </div>

        <div className="bg-blue-500/10 border border-blue-500/30 rounded-xl p-4 mb-8">
          <p className="text-blue-300">Pass requirement: <span className="font-bold">70%</span></p>
          <p className="text-slate-400 text-sm mt-1">Score 7 or more correct answers to unlock the next level.</p>
        </div>

        {error && <div className="bg-red-500/10 border border-red-500/30 text-red-400 p-4 rounded-lg mb-6">{error}</div>}
        {loading && <p className="text-slate-400">Loading questions…</p>}

        {questions.map((q, index) => (
          <div key={q.id} className="bg-slate-900 border border-slate-800 rounded-xl p-6 mb-6">
            <p className="text-lg font-semibold mb-5">{index + 1}. {q.question_text}</p>
            <div className="space-y-3">
              {["A", "B", "C", "D"].map((opt) => (
                <button
                  key={opt}
                  onClick={() => setAnswers((a) => ({ ...a, [q.id]: opt }))}
                  className={`w-full text-left p-4 rounded-lg border transition ${
                    answers[q.id] === opt ? "border-blue-500 bg-blue-500/20" : "border-slate-700 hover:bg-slate-800"
                  }`}
                >
                  <b>{opt}.</b> {q[`option_${opt.toLowerCase()}`]}
                </button>
              ))}
            </div>
          </div>
        ))}

        {questions.length > 0 && (
          <button
            onClick={finish}
            disabled={submitting || answered !== questions.length}
            className="w-full bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 disabled:text-slate-400 py-4 rounded-xl font-bold text-lg"
          >
            {submitting
              ? "Submitting…"
              : answered === questions.length
              ? `Submit Level ${level} Assessment`
              : `Answer all questions to submit (${questions.length - answered} left)`}
          </button>
        )}
      </div>
    </div>
  );
}
