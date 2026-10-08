export const inputClass =
  "w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 outline-none focus:border-blue-500";

export function Field({ label, children }) {
  return (
    <div className="mb-5">
      <label className="block text-sm text-slate-300 mb-2">{label}</label>
      {children}
    </div>
  );
}

export function AuthShell({ title, subtitle, error, children }) {
  return (
    <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center px-6 py-10">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold">{title}</h1>
          <p className="text-slate-400 mt-2">{subtitle}</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8">
          {error && (
            <div className="bg-red-500/10 border border-red-500/30 text-red-400 p-3 rounded-lg mb-5 text-sm">
              {error}
            </div>
          )}
          {children}
        </div>
      </div>
    </div>
  );
}
