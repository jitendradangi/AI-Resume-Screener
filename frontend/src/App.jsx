import { Routes, Route } from "react-router-dom";

import Login from "./pages/login";
import Register from "./pages/register";
import Dashboard from "./pages/dashboard";
import UploadResume from "./pages/UploadResume";
import MyResumes from "./pages/MyResumes";
import ResumeDetails from "./pages/ResumeDetails";
import ATSScore from "./pages/ATSScore";
import Jobs from "./pages/jobs";
import MatchDetails from "./pages/MatchDetails";
import Profile from "./pages/Profile";

import ProtectedRoute from "./routers/ProtectedRoute";

function App() {
  return (
    <Routes>

      <Route path="/" element={<Login />} />

      <Route path="/register" element={<Register />} />

      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />

      <Route
        path="/upload"
        element={
          <ProtectedRoute>
            <UploadResume />
          </ProtectedRoute>
        }
      />

      <Route
        path="/my-resumes"
        element={
          <ProtectedRoute>
            <MyResumes />
          </ProtectedRoute>
        }
      />

      <Route
        path="/resume/:public_id"
        element={
          <ProtectedRoute>
            <ResumeDetails />
          </ProtectedRoute>
        }
      />

      <Route
        path="/ats-score/:public_id"
        element={
          <ProtectedRoute>
            <ATSScore />
          </ProtectedRoute>
        }
      />

      <Route
        path="/ats-score"
        element={
          <ProtectedRoute>
            <ATSScore />
          </ProtectedRoute>
        }
      />

      <Route
        path="/jobs"
        element={
          <ProtectedRoute>
            <Jobs />
          </ProtectedRoute>
        }
      />

      <Route
        path="/match/:resumePublicId/:jobPublicId"
        element={
          <ProtectedRoute>
            <MatchDetails />
          </ProtectedRoute>
        }
      />

      <Route
        path="/profile"
        element={
          <ProtectedRoute>
            <Profile />
          </ProtectedRoute>
        }
      />

    </Routes>
  );
}

export default App;