import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getProgress, getSubjects } from "../services/api";
import { DIFFICULTIES, LEVEL_NAMES } from "../lib";

export default function Dashboard() {
  const navigate = useNavigate();
  const [subjects, setSubjects] = useState([]);
  const [progress, setProgress] = useState({});
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    Promise.all([getSubjects(), getProgress()])
      .then(([s, p]) => {
        if (cancelled) return;
        setSubjects(s);
        setProgress(p.highest_passed || {});
      })
      .catch((e) => !cancelled && setError(e.message))
      .finally(() => !cancelled && setLoading(false));
    return () => { cancelled = true; };
  }, []);

  const start = (subject, level) => navigate("/assessment", { state: { subject, level } });

  if (loading) return <p className="text-slate-400">Loading your dashboard…</p>;

  return (
    <>
      <h1 className="text-4xl font-bold">Your Skill Dashboard</h1>
      <p className="text-slate-400 mt-2 mb-10">Choose a subject and progress through three difficulty levels.</p>

      {error && <div className="bg-red-500/10 border border-red-500/30 text-red-400 p-4 rounded-lg mb-6">{error}</div>}

      <div className="space-y-8">
        {subjects.map((subject) => {
          const highest = progress[String(subject.id)] || 0;
          return (
            <section key={subject.id} className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
              <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <div>
                  <h2 className="text-2xl font-bold">{subject.name}</h2>
                  <p className="text-slate-400 mt-2">{subject.description}</p>
                  <p className="text-sm text-slate-500 mt-3">{subject.topics.length} topics</p>
                </div>
                <div className="text-sm text-slate-400">
                  Highest passed level:{" "}
                  <span className="text-white font-semibold">{highest === 0 ? "None" : `Level ${highest}`}</span>
                </div>
              </div>

              <div className="grid md:grid-cols-3 gap-4 mt-6">
                {[1, 2, 3].map((level) => {
                  const passed = highest >= level;
                  const unlocked = level <= highest + 1;
                  const tone = passed
                    ? "border-emerald-500/40 bg-emerald-500/10"
                    : unlocked
                    ? "border-blue-500/40 bg-blue-500/10"
                    : "border-slate-800 bg-slate-950/50";
                  return (
                    <div key={level} className={`rounded-xl border p-5 ${tone}`}>
                      <p className="text-sm text-slate-400">Level {level}</p>
                      <h3 className="text-xl font-bold mt-1">{LEVEL_NAMES[level]}</h3>
                      <p className="text-sm text-slate-400 mt-3">{DIFFICULTIES[level]} questions • 10 questions</p>
                      <p className="text-xs text-slate-500 mt-2">70% required to pass</p>

                      {passed ? (
                        <div className="mt-5">
                          <p className="text-sm font-semibold text-emerald-400 mb-3">Level Passed</p>
                          <button onClick={() => start(subject, level)}
                                  className="w-full bg-slate-800 hover:bg-slate-700 py-3 rounded-lg font-semibold">
                            Retake Level
                          </button>
                        </div>
                      ) : unlocked ? (
                        <button onClick={() => start(subject, level)}
                                className="w-full mt-5 bg-blue-600 hover:bg-blue-500 py-3 rounded-lg font-semibold">
                          Start Level {level}
                        </button>
                      ) : (
                        <p className="mt-5 text-center text-sm text-slate-500">Pass Level {level - 1} first</p>
                      )}
                    </div>
                  );
                })}
              </div>
            </section>
          );
        })}
      </div>
    </>
  );
}
