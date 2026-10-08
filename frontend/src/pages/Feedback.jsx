import { useEffect, useState } from "react";
import { getMyFeedback, submitFeedback } from "../services/api";

export const CATEGORIES = [
  ["General", "General"],
  ["Assessment", "Assessment"],
  ["Questions", "Questions"],
  ["UI/Experience", "UI / Experience"],
  ["Technical Issue", "Technical Issue"],
];

export const Stars = ({ rating }) => (
  <span className="text-yellow-400 text-xl">{"★".repeat(rating)}{"☆".repeat(5 - rating)}</span>
);

export default function Feedback() {
  const [list, setList] = useState([]);
  const [rating, setRating] = useState(0);
  const [category, setCategory] = useState("General");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    getMyFeedback().then(setList).catch((e) => setError(e.message));
  }, []);

  async function submit(e) {
    e.preventDefault();
    setError(""); setNotice("");
    if (rating < 1) return setError("Please select a rating from 1 to 5.");
    if (!message.trim()) return setError("Please enter your feedback.");
    setBusy(true);
    try {
      await submitFeedback(rating, category, message);
      setRating(0); setCategory("General"); setMessage("");
      setNotice("Thank you! Your feedback has been submitted.");
      setList(await getMyFeedback());
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-4xl font-bold">Feedback</h1>
      <p className="text-slate-400 mt-2 mb-10">Share your experience and help us improve CodeCompass.</p>

      <form onSubmit={submit} className="bg-slate-900 border border-slate-800 rounded-2xl p-8">
        <h2 className="text-2xl font-bold">Give Feedback</h2>
        {error && <div className="bg-red-500/10 border border-red-500/30 text-red-400 p-3 rounded-lg mt-5 text-sm">{error}</div>}
        {notice && <div className="bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 p-3 rounded-lg mt-5 text-sm">{notice}</div>}

        <div className="mt-8">
          <label className="block text-slate-300 mb-3">Rate your experience</label>
          <div className="flex gap-2">
            {[1, 2, 3, 4, 5].map((s) => (
              <button key={s} type="button" aria-label={`Rate ${s} out of 5`} onClick={() => setRating(s)}
                      className={`text-4xl transition ${s <= rating ? "text-yellow-400" : "text-slate-600 hover:text-yellow-300"}`}>
                ★
              </button>
            ))}
          </div>
          <p className="text-sm text-slate-500 mt-2">{rating === 0 ? "Select a rating" : `${rating} out of 5`}</p>
        </div>

        <div className="mt-8">
          <label className="block text-slate-300 mb-2">Category</label>
          <select value={category} onChange={(e) => setCategory(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-3 text-white">
            {CATEGORIES.map(([value, label]) => <option key={value} value={value}>{label}</option>)}
          </select>
        </div>

        <div className="mt-8">
          <label className="block text-slate-300 mb-2">Your feedback</label>
          <textarea value={message} onChange={(e) => setMessage(e.target.value)} rows={6} maxLength={2000}
                    placeholder="Tell us about your experience..."
                    className="w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-3 text-white resize-none" />
          <p className="text-xs text-slate-500 mt-2 text-right">{message.length}/2000</p>
        </div>

        <button type="submit" disabled={busy}
                className="mt-8 bg-blue-600 hover:bg-blue-500 disabled:bg-blue-800 px-8 py-3 rounded-lg font-semibold">
          {busy ? "Submitting…" : "Submit Feedback"}
        </button>
      </form>

      <h2 className="text-2xl font-bold mt-10 mb-5">My Previous Feedback</h2>
      {list.length === 0 ? (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 text-slate-400">You haven't submitted any feedback yet.</div>
      ) : (
        <div className="space-y-4">
          {list.map((f) => (
            <div key={f.id} className="bg-slate-900 border border-slate-800 rounded-xl p-6">
              <div className="flex flex-col sm:flex-row sm:justify-between gap-3">
                <div>
                  <Stars rating={f.rating} />
                  <p className="text-sm text-blue-400 mt-2">{f.category}</p>
                </div>
                <p className="text-sm text-slate-500">{new Date(f.created_at).toLocaleDateString()}</p>
              </div>
              <p className="text-slate-300 mt-4 leading-relaxed whitespace-pre-wrap">{f.message}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
