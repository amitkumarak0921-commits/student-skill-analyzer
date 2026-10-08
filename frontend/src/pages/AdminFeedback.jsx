import { useEffect, useState } from "react";
import { getAllFeedback } from "../services/api";
import { Stars } from "./Feedback";

export default function AdminFeedback() {
  const [items, setItems] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    getAllFeedback().then((d) => setItems(d.feedback)).catch((e) => setError(e.message));
  }, []);

  const average = items.length ? (items.reduce((s, f) => s + f.rating, 0) / items.length).toFixed(1) : "0.0";

  return (
    <>
      <p className="text-blue-400 font-semibold">Admin Panel</p>
      <h1 className="text-4xl font-bold mt-1">All Student Feedback</h1>
      <p className="text-slate-400 mt-2 mb-10">Review feedback submitted by students.</p>

      {error && <div className="bg-red-500/10 border border-red-500/30 text-red-400 p-4 rounded-lg mb-6">{error}</div>}

      <div className="grid md:grid-cols-3 gap-5 mb-8">
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
          <p className="text-slate-400">Total Feedback</p>
          <p className="text-4xl font-bold text-blue-400 mt-2">{items.length}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
          <p className="text-slate-400">Average Rating</p>
          <p className="text-4xl font-bold text-yellow-400 mt-2">{average}<span className="text-lg text-slate-500"> / 5</span></p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
          <p className="text-slate-400">Latest Feedback</p>
          <p className="text-lg font-semibold mt-3">{items.length ? new Date(items[0].created_at).toLocaleDateString() : "No feedback"}</p>
        </div>
      </div>

      {items.length === 0 ? (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 text-center text-slate-400">No feedback has been submitted yet.</div>
      ) : (
        <div className="space-y-5">
          {items.map((f) => (
            <div key={f.id} className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
              <div className="flex flex-col md:flex-row md:justify-between gap-4">
                <div>
                  <p className="font-semibold text-lg">{f.user_name || "Student"}</p>
                  {f.user_email && <p className="text-sm text-slate-500 mt-1">{f.user_email}</p>}
                  <div className="mt-3"><Stars rating={f.rating} /></div>
                </div>
                <p className="text-sm text-slate-500">{new Date(f.created_at).toLocaleString()}</p>
              </div>
              <span className="inline-block mt-5 bg-blue-500/10 border border-blue-500/30 text-blue-400 px-3 py-1 rounded-full text-sm">{f.category}</span>
              <p className="text-slate-300 leading-relaxed mt-5 whitespace-pre-wrap">{f.message}</p>
            </div>
          ))}
        </div>
      )}
    </>
  );
}
