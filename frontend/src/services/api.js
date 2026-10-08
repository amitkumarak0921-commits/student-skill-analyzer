const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export const getToken = () => localStorage.getItem("token");
export const setToken = (t) => localStorage.setItem("token", t);
export const clearToken = () => localStorage.removeItem("token");

export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
  }
}

function messageFrom(data, fallback) {
  const d = data?.detail;
  if (typeof d === "string") return d;
  if (Array.isArray(d) && d.length) {
    // FastAPI validation errors
    return d.map((e) => `${(e.loc || []).slice(1).join(".")}: ${e.msg}`).join("; ");
  }
  return fallback;
}

async function request(path, { method = "GET", body, auth = true } = {}) {
  const headers = {};
  if (body !== undefined) headers["Content-Type"] = "application/json";
  if (auth && getToken()) headers.Authorization = `Bearer ${getToken()}`;

  let response;
  try {
    response = await fetch(`${API_URL}${path}`, {
      method,
      headers,
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });
  } catch {
    throw new ApiError("Cannot reach the server. Is the backend running?", 0);
  }

  let data = null;
  try {
    data = await response.json();
  } catch {
    /* empty body */
  }
  if (!response.ok) {
    throw new ApiError(messageFrom(data, `Request failed (${response.status})`), response.status);
  }
  return data;
}

// Auth
export const registerUser = (form) => request("/api/auth/register", { method: "POST", body: form, auth: false });
export const loginUser = (email, password) =>
  request("/api/auth/login", { method: "POST", body: { email, password }, auth: false });
export const getCurrentUser = () => request("/api/auth/me");

// Subjects & assessments
export const getSubjects = () => request("/api/subjects", { auth: false });
export const getProgress = () => request("/api/questions/progress");
export const startAssessment = (subjectId, level) => request(`/api/questions/subject/${subjectId}?level=${level}`);
export const submitAssessment = (sessionToken, answers) =>
  request("/api/questions/submit", { method: "POST", body: { session_token: sessionToken, answers } });

// Feedback
export const submitFeedback = (rating, category, message) =>
  request("/api/feedback/my", { method: "POST", body: { rating, category, message } });
export const getMyFeedback = () => request("/api/feedback/my");
export const getAllFeedback = () => request("/api/feedback");
