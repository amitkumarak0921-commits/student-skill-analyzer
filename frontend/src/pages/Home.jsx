import { Link, Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { Spinner } from "../components/Layout";

export default function Home() {
  const { user, loading } = useAuth();
  if (loading) return <Spinner />;
  if (user) return <Navigate to="/dashboard" replace />;

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <nav className="flex items-center justify-between px-8 py-5 border-b border-slate-800">
        <h1 className="text-2xl font-bold text-blue-400">CodeCompass</h1>
        <div className="flex gap-4">
          <Link to="/login" className="px-5 py-2 rounded-lg border border-slate-700 hover:bg-slate-800">Login</Link>
          <Link to="/register" className="px-5 py-2 rounded-lg bg-blue-600 hover:bg-blue-500">Get Started</Link>
        </div>
      </nav>
      <main className="flex flex-col items-center text-center px-6 py-32">
        <h2 className="text-5xl font-bold max-w-3xl">
          Know Your Skills. <span className="text-blue-400">Find Your Gaps.</span>
        </h2>
        <p className="text-slate-400 text-lg max-w-2xl mt-6">
          Take level-by-level assessments in C, Java and DBMS, see exactly which topics need work,
          and know what to study next.
        </p>
        <Link to="/register" className="mt-8 bg-blue-600 hover:bg-blue-500 px-8 py-4 rounded-xl font-semibold text-lg">
          Start Your Assessment
        </Link>
      </main>
    </div>
  );
}
