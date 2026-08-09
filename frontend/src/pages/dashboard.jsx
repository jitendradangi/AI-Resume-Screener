import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import DashboardLayout from "../layouts/DashboardLayout";
import { FaFilePdf, FaFileWord, FaUpload, FaTrophy, FaBriefcase, FaArrowRight, FaSpinner } from "react-icons/fa";
import { getMyResumes } from "../services/resumeService";
import { getJobRecommendations } from "../services/jobService";

const formatFilename = (filename) => {
  if (!filename) return "";
  const parts = filename.split('_');
  if (parts.length > 1 && parts[0].length === 36) {
    return parts.slice(1).join('_');
  }
  return filename;
};

const getFileIcon = (filename) => {
  const extension = filename.split(".").pop().toLowerCase();
  switch (extension) {
    case "pdf":
      return <FaFilePdf color="#e53935" size={24} />;
    case "doc":
    case "docx":
      return <FaFileWord color="#1565c0" size={24} />;
    default:
      return null;
  }
};

const getScoreColor = (score) => {
  if (score >= 80) return "text-emerald-600 dark:text-emerald-400";
  if (score >= 60) return "text-amber-600 dark:text-amber-400";
  return "text-rose-600 dark:text-rose-400";
};

const getScoreBgColor = (score) => {
  if (score >= 80) return "bg-emerald-100 dark:bg-emerald-900/30 border-emerald-200 dark:border-emerald-900/50";
  if (score >= 60) return "bg-amber-100 dark:bg-amber-900/30 border-amber-200 dark:border-amber-900/50";
  return "bg-rose-100 dark:bg-rose-900/30 border-rose-200 dark:border-rose-900/50";
};

const getScoreLabel = (score) => {
  if (score >= 80) return "Excellent";
  if (score >= 60) return "Good";
  if (score >= 40) return "Fair";
  return "Needs Improvement";
};

function Dashboard() {
  const navigate = useNavigate();
  const [resumes, setResumes] = useState([]);
  const [latestResume, setLatestResume] = useState(null);
  const [jobMatches, setJobMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        setError("");
        
        // Fetch resumes
        const resumesData = await getMyResumes();
        setResumes(resumesData);
        
        // Set latest resume
        if (resumesData.length > 0) {
          const latest = resumesData.sort((a, b) => 
            new Date(b.uploaded_at) - new Date(a.uploaded_at)
          )[0];
          setLatestResume(latest);
          
          // Fetch job recommendations for latest resume
          try {
            const matches = await getJobRecommendations(latest.public_id, 5, 50);
            setJobMatches(matches);
          } catch (matchErr) {
            console.error("Failed to fetch job matches:", matchErr);
            setJobMatches([]);
          }
        }
      } catch (err) {
        setError("Failed to load dashboard data");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const getLatestATSScore = () => {
    if (!latestResume || !latestResume.ai_analysis) return null;
    return latestResume.ai_analysis.overall_score;
  };

  const getBestMatchPercentage = () => {
    if (jobMatches.length === 0) return 0;
    return Math.max(...jobMatches.map(match => match.overall_match));
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="max-w-6xl mx-auto py-8">
          <div className="flex items-center gap-2 text-slate-600 dark:text-slate-400">
            <FaSpinner className="animate-spin" />
            <span>Loading dashboard...</span>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  if (error) {
    return (
      <DashboardLayout>
        <div className="max-w-6xl mx-auto py-8">
          <div className="bg-rose-50 dark:bg-rose-900/30 border border-rose-200 dark:border-rose-900/50 rounded-lg p-6">
            <p className="text-rose-700 dark:text-rose-400 font-medium">{error}</p>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  const latestATSScore = getLatestATSScore();
  const bestMatchPercentage = getBestMatchPercentage();

  return (
    <DashboardLayout>
      <div className="max-w-6xl mx-auto py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Dashboard</h1>
          <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">
            Welcome to AI Resume Screener. Track your resume performance and job matches.
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 mb-8">
          {/* Resume Count */}
          <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-medium text-slate-500 dark:text-slate-400">Total Resumes</h3>
              <div className="p-2 bg-indigo-100 dark:bg-indigo-900/30 rounded-lg">
                <FaFilePdf className="text-indigo-600 dark:text-indigo-400" size={20} />
              </div>
            </div>
            <p className="text-3xl font-bold text-slate-900 dark:text-white">{resumes.length}</p>
            <p className="mt-2 text-xs text-slate-500 dark:text-slate-400">
              {resumes.length === 1 ? 'resume uploaded' : 'resumes uploaded'}
            </p>
          </div>

          {/* ATS Score */}
          <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-medium text-slate-500 dark:text-slate-400">Latest ATS Score</h3>
              <div className="p-2 bg-emerald-100 dark:bg-emerald-900/30 rounded-lg">
                <FaTrophy className="text-emerald-600 dark:text-emerald-400" size={20} />
              </div>
            </div>
            {latestATSScore !== null ? (
              <>
                <p className={`text-3xl font-bold ${getScoreColor(latestATSScore)}`}>
                  {latestATSScore}
                </p>
                <div className="mt-2 flex items-center gap-2">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getScoreBgColor(latestATSScore)} ${getScoreColor(latestATSScore)}`}>
                    {getScoreLabel(latestATSScore)}
                  </span>
                  <span className="text-xs text-slate-500 dark:text-slate-400">/ 100</span>
                </div>
              </>
            ) : (
              <>
                <p className="text-3xl font-bold text-slate-400 dark:text-slate-600">-</p>
                <p className="mt-2 text-xs text-slate-500 dark:text-slate-400">No analysis yet</p>
              </>
            )}
          </div>

          {/* Job Matches */}
          <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-medium text-slate-500 dark:text-slate-400">Job Matches</h3>
              <div className="p-2 bg-amber-100 dark:bg-amber-900/30 rounded-lg">
                <FaBriefcase className="text-amber-600 dark:text-amber-400" size={20} />
              </div>
            </div>
            <p className="text-3xl font-bold text-slate-900 dark:text-white">{jobMatches.length}</p>
            <p className="mt-2 text-xs text-slate-500 dark:text-slate-400">
              {jobMatches.length > 0 ? `Best match: ${Math.round(bestMatchPercentage)}%` : 'No matches yet'}
            </p>
          </div>
        </div>

        {/* Latest Resume Card */}
        {latestResume && (
          <div className="mb-8 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-slate-900 dark:text-white">Latest Resume</h3>
              <button
                onClick={() => navigate(`/resume/${latestResume.public_id}`)}
                className="text-indigo-600 dark:text-indigo-400 hover:text-indigo-700 dark:hover:text-indigo-300 text-sm font-medium flex items-center gap-1"
              >
                View Details <FaArrowRight size={14} />
              </button>
            </div>
            <div className="flex items-start gap-4">
              <div className="flex-shrink-0">
                {getFileIcon(latestResume.original_filename)}
              </div>
              <div className="flex-grow">
                <h4 className="text-base font-medium text-slate-900 dark:text-white mb-1">
                  {formatFilename(latestResume.original_filename)}
                </h4>
                <div className="flex items-center gap-4 text-sm text-slate-500 dark:text-slate-400">
                  <span>Uploaded: {new Date(latestResume.uploaded_at).toLocaleDateString()}</span>
                  <span className={`font-medium ${
                    latestResume.processing_status === 'completed' 
                      ? 'text-emerald-600 dark:text-emerald-400' 
                      : latestResume.processing_status === 'failed'
                      ? 'text-rose-600 dark:text-rose-400'
                      : 'text-amber-600 dark:text-amber-400'
                  }`}>
                    {latestResume.processing_status.charAt(0).toUpperCase() + latestResume.processing_status.slice(1)}
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Quick Actions */}
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm p-6">
          <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-4">Quick Actions</h3>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <button
              onClick={() => navigate("/upload")}
              className="flex items-center justify-center gap-3 px-6 py-4 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 transition-colors"
            >
              <FaUpload />
              <span>Upload Resume</span>
            </button>
            <button
              onClick={() => latestResume ? navigate(`/ats-score/${latestResume.public_id}`) : navigate("/my-resumes")}
              disabled={!latestResume}
              className="flex items-center justify-center gap-3 px-6 py-4 bg-emerald-600 text-white font-medium rounded-lg hover:bg-emerald-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <FaTrophy />
              <span>View ATS Score</span>
            </button>
            <button
              onClick={() => latestResume ? navigate(`/jobs?resume=${latestResume.public_id}`) : navigate("/jobs")}
              disabled={resumes.length === 0}
              className="flex items-center justify-center gap-3 px-6 py-4 bg-amber-600 text-white font-medium rounded-lg hover:bg-amber-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <FaBriefcase />
              <span>Find Matching Jobs</span>
            </button>
          </div>
        </div>

        {/* Empty State */}
        {resumes.length === 0 && (
          <div className="mt-8 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-12 text-center shadow-sm">
            <h3 className="text-lg font-medium text-slate-900 dark:text-white mb-2">No Resumes Yet</h3>
            <p className="text-slate-500 dark:text-slate-400 mb-6">
              Upload your first resume to get started with ATS analysis and job matching.
            </p>
            <button
              onClick={() => navigate("/upload")}
              className="px-6 py-3 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 transition-colors flex items-center gap-2 mx-auto"
            >
              <FaUpload />
              <span>Upload Resume</span>
            </button>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}

export default Dashboard;
