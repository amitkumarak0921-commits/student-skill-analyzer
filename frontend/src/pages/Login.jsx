import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { AuthShell, Field, inputClass } from "../components/AuthForm";

export default function Login() {
  const { user, login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  if (user) return <Navigate to="/dashboard" replace />;

  async function submit(e) {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      await login(email, password);
      navigate("/dashboard", { replace: true });
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <AuthShell title="Welcome Back" subtitle="Login to your CodeCompass account" error={error}>
      <form onSubmit={submit}>
        <Field label="Email">
          <input type="email" required value={email} onChange={(e) => setEmail(e.target.value)}
                 placeholder="Enter your email" className={inputClass} />
        </Field>
        <Field label="Password">
          <input type="password" required value={password} onChange={(e) => setPassword(e.target.value)}
                 placeholder="Enter your password" className={inputClass} />
        </Field>
        <button type="submit" disabled={busy}
                className="w-full bg-blue-600 hover:bg-blue-500 disabled:bg-blue-800 py-3 rounded-lg font-semibold">
          {busy ? "Logging in..." : "Login"}
        </button>
        <p className="text-center text-slate-400 mt-6">
          Don't have an account? <Link to="/register" className="text-blue-400 hover:text-blue-300">Create Account</Link>
        </p>
      </form>
    </AuthShell>
  );
}
