import { Link, NavLink, Navigate, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const link = ({ isActive }) =>
  isActive ? "text-blue-400 font-semibold" : "text-slate-300 hover:text-white";

export function Spinner() {
  return <div className="min-h-screen flex items-center justify-center text-slate-400">Loading…</div>;
}

export function ProtectedLayout({ adminOnly = false }) {
  const { user, loading, logout } = useAuth();
  const navigate = useNavigate();

  if (loading) return <Spinner />;
  if (!user) return <Navigate to="/login" replace />;
  if (adminOnly && user.role !== "ADMIN") return <Navigate to="/dashboard" replace />;

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <nav className="border-b border-slate-800 px-8 py-5 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <Link to="/dashboard" className="text-2xl font-bold text-blue-400">CodeCompass</Link>
        <div className="flex flex-wrap gap-5 items-center">
          <NavLink to="/dashboard" className={link}>Dashboard</NavLink>
          <NavLink to="/feedback" className={link}>Feedback</NavLink>
          {user.role === "ADMIN" && <NavLink to="/admin/feedback" className={link}>All Feedback</NavLink>}
          <span className="text-slate-300">Hi, {user.name}</span>
          <button
            onClick={() => { logout(); navigate("/"); }}
            className="text-slate-400 hover:text-white"
          >
            Logout
          </button>
        </div>
      </nav>
      <main className="max-w-6xl mx-auto px-6 py-10">
        <Outlet />
      </main>
    </div>
  );
}
