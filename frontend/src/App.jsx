import { Navigate, Outlet, Route, Routes } from "react-router-dom";
import { useAuth } from "./context/AuthContext";
import { ProtectedLayout, Spinner } from "./components/Layout";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Assessment from "./pages/Assessment";
import Result from "./pages/Result";
import Feedback from "./pages/Feedback";
import AdminFeedback from "./pages/AdminFeedback";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      <Route element={<ProtectedLayout />}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/feedback" element={<Feedback />} />
      </Route>
      <Route element={<ProtectedLayout adminOnly />}>
        <Route path="/admin/feedback" element={<AdminFeedback />} />
      </Route>

      {/* Full-screen pages that still require login */}
      <Route element={<ProtectedFull />}>
        <Route path="/assessment" element={<Assessment />} />
        <Route path="/result" element={<Result />} />
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

function ProtectedFull() {
  const { user, loading } = useAuth();
  if (loading) return <Spinner />;
  if (!user) return <Navigate to="/login" replace />;
  return <Outlet />;
}
