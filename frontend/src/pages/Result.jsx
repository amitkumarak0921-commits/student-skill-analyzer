import { Link, Navigate, useLocation, useNavigate } from "react-router-dom";
import { Cell, Pie, PieChart, PolarAngleAxis, PolarGrid, PolarRadiusAxis, Radar, RadarChart, ResponsiveContainer, Tooltip } from "recharts";
import { DIFFICULTIES } from "../lib";

function recommend(topic) {
  if (topic.percentage < 50) return `Start with the basics of ${topic.topic} and practice simple questions.`;
  if (topic.percentage < 75) return `Revise ${topic.topic} and solve more practice questions.`;
  return `You are doing well in ${topic.topic}. Try advanced problems to improve further.`;
}

const Card = ({ label, children }) => (
  <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
    <p className="text-slate-400">{label}</p>
    {children}
  </div>
);

export default function Result() {
  const { state } = useLocation();
  const navigate = useNavigate();
  const result = state?.result;
  const subject = state?.subject;
  if (!result || !subject) return <Navigate to="/dashboard" replace />;

  const topics = result.topic_results;
  const weakest = topics.length ? topics.reduce((w, c) => (c.percentage < w.percentage ? c : w)) : null;

  return (
    <div className="min-h-screen bg-slate-950 text-white p-8">
      <div className="max-w-6xl mx-auto">
        <Link to="/dashboard" className="text-slate-400 hover:text-white inline-block mb-6">← Back to Dashboard</Link>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
          <p className="text-blue-400 font-semibold">Level {result.level}</p>
          <h1 className="text-4xl font-bold mt-1">{subject.name}</h1>
          <p className="text-slate-400 mt-2">{result.level_name} • {DIFFICULTIES[result.level]} Assessment</p>
        </div>

        <div className={`mt-6 rounded-2xl p-6 border ${result.passed ? "bg-emerald-500/10 border-emerald-500/30" : "bg-red-500/10 border-red-500/30"}`}>
          <p className={`text-2xl font-bold ${result.passed ? "text-emerald-400" : "text-red-400"}`}>
            {result.passed ? "Level Passed" : "Level Not Passed"}
          </p>
          <p className="text-slate-400 mt-2">
            {result.passed
              ? result.next_level
                ? `Great work! Level ${result.next_level} is now unlocked.`
                : "You have completed all three assessment levels."
              : "You need at least 70% to pass this level. You can try this level again."}
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-5 mt-8">
          <Card label="Level Score"><p className="text-4xl font-bold mt-2 text-blue-400">{result.percentage}%</p></Card>
          <Card label="Correct Answers"><p className="text-4xl font-bold mt-2">{result.correct}/{result.total}</p></Card>
          <Card label="Level"><p className="text-3xl font-bold mt-2 text-blue-400">{result.level_name}</p></Card>
        </div>

        <div className="grid lg:grid-cols-2 gap-6 mt-8">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
            <h2 className="text-2xl font-bold mb-4">Level Performance</h2>
            <div className="h-80 relative">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={[{ name: "Score", value: result.percentage }, { name: "Remaining", value: 100 - result.percentage }]}
                       innerRadius={80} outerRadius={110} dataKey="value" startAngle={90} endAngle={-270} stroke="none">
                    <Cell fill="#3b82f6" />
                    <Cell fill="#1e293b" />
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
              <div className="absolute inset-0 flex items-center justify-center pointer-events-none text-3xl font-bold">
                {result.percentage}%
              </div>
            </div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
            <h2 className="text-2xl font-bold mb-4">Topic Performance</h2>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart data={topics.map((t) => ({ topic: t.topic, score: t.percentage }))}>
                  <PolarGrid stroke="#334155" />
                  <PolarAngleAxis dataKey="topic" tick={{ fill: "#cbd5e1", fontSize: 12 }} />
                  <PolarRadiusAxis domain={[0, 100]} tick={{ fill: "#64748b" }} />
                  <Radar name="Score" dataKey="score" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.5} />
                  <Tooltip />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {weakest && (
          <div className="mt-8 grid md:grid-cols-2 gap-6">
            <Card label="Your Next Focus">
              <h2 className="text-3xl font-bold mt-2">{weakest.topic}</h2>
              <p className="text-slate-400 mt-3">Current performance: {weakest.percentage}%</p>
            </Card>
            <Card label="Recommended Action"><p className="text-lg mt-3">{recommend(weakest)}</p></Card>
          </div>
        )}

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 mt-8">
          <h2 className="text-2xl font-bold mb-6">Detailed Topic Analysis</h2>
          <div className="space-y-5">
            {topics.map((t) => (
              <div key={t.topic}>
                <div className="flex justify-between mb-2">
                  <span>{t.topic} <span className="text-slate-500 text-sm">({t.correct}/{t.total})</span></span>
                  <span>{t.percentage}%</span>
                </div>
                <div className="h-3 bg-slate-800 rounded-full">
                  <div className="h-3 bg-blue-500 rounded-full" style={{ width: `${t.percentage}%` }} />
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="flex flex-col sm:flex-row gap-4 mt-8">
          <Link to="/dashboard" className="bg-blue-600 hover:bg-blue-500 px-6 py-3 rounded-lg text-center">Back to Dashboard</Link>
          {!result.passed && (
            <button
              onClick={() => navigate("/assessment", { state: { subject, level: result.level }, replace: true })}
              className="bg-slate-800 hover:bg-slate-700 px-6 py-3 rounded-lg"
            >
              Retry Level {result.level}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
