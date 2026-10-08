import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { AuthShell, Field, inputClass } from "../components/AuthForm";

export default function Register() {
  const { user, register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: "", email: "", password: "", college: "", branch: "", semester: "" });
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  if (user) return <Navigate to="/dashboard" replace />;

  const set = (key) => (e) => setForm((f) => ({ ...f, [key]: e.target.value }));

  async function submit(e) {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      await register(form);
      navigate("/dashboard", { replace: true });
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <AuthShell title="Create your account" subtitle="Start understanding your technical skills." error={error}>
      <form onSubmit={submit}>
        <Field label="Full Name">
          <input required maxLength={100} value={form.name} onChange={set("name")} placeholder="Enter your name" className={inputClass} />
        </Field>
        <Field label="Email">
          <input type="email" required value={form.email} onChange={set("email")} placeholder="Enter your email" className={inputClass} />
        </Field>
        <Field label="Password (6–72 characters)">
          <input type="password" required minLength={6} maxLength={72} value={form.password}
                 onChange={set("password")} placeholder="Create a password" className={inputClass} />
        </Field>
        <Field label="College (optional)">
          <input maxLength={150} value={form.college} onChange={set("college")} className={inputClass} />
        </Field>
        <div className="grid grid-cols-2 gap-4">
          <Field label="Branch (optional)">
            <input maxLength={100} value={form.branch} onChange={set("branch")} className={inputClass} />
          </Field>
          <Field label="Semester (optional)">
            <input maxLength={30} value={form.semester} onChange={set("semester")} className={inputClass} />
          </Field>
        </div>
        <button type="submit" disabled={busy}
                className="w-full bg-blue-600 hover:bg-blue-500 disabled:bg-blue-800 py-3 rounded-lg font-semibold">
          {busy ? "Creating Account..." : "Create Account"}
        </button>
        <p className="text-center text-slate-400 text-sm mt-6">
          Already have an account? <Link to="/login" className="text-blue-400 hover:text-blue-300">Login</Link>
        </p>
      </form>
      <Link to="/" className="block text-center mt-6 text-slate-500 hover:text-slate-300 text-sm">← Back to home</Link>
    </AuthShell>
  );
}
