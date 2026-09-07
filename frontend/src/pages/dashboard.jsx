import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import DashboardLayout from "../layouts/DashboardLayout";
import { 
  FaFilePdf, 
  FaFileWord, 
  FaUpload, 
  FaTrophy, 
  FaBriefcase, 
  FaArrowRight, 
  FaSpinner,
  FaCheckCircle,
  FaExclamationTriangle,
  FaClock
} from "react-icons/fa";
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
      return <FaFilePdf className="text-rose-500 text-xl sm:text-2xl" />;
    case "doc":
    case "docx":
      return <FaFileWord className="text-blue-500 text-xl sm:text-2xl" />;
    default:
      return <FaFilePdf className="text-indigo-400 text-xl sm:text-2xl" />;
  }
};

const getScoreColor = (score) => {
  if (score >= 80) return "text-emerald-400";
  if (score >= 60) return "text-amber-400";
  return "text-rose-400";
};

const getScoreBgColor = (score) => {
  if (score >= 80) return "bg-emerald-500/10 border-emerald-500/20 text-emerald-400";
  if (score >= 60) return "bg-amber-500/10 border-amber-500/20 text-amber-400";
  return "bg-rose-500/10 border-rose-500/20 text-rose-400";
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
        <div className="max-w-6xl mx-auto py-12 flex items-center justify-center min-h-[400px]">
          <div className="flex items-center gap-3 px-5 py-3 rounded-2xl bg-slate-900/80 border border-slate-800 text-indigo-400 text-sm font-medium shadow-xl backdrop-blur-xl">
            <FaSpinner className="animate-spin text-base" />
            <span>Loading your dashboard...</span>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  if (error) {
    return (
      <DashboardLayout>
        <div className="max-w-6xl mx-auto py-8">
          <div className="bg-rose-500/10 border border-rose-500/20 rounded-2xl p-6 backdrop-blur-xl text-center">
            <p className="text-rose-300 text-sm font-medium">{error}</p>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  const latestATSScore = getLatestATSScore();
  const bestMatchPercentage = getBestMatchPercentage();

  return (
    <DashboardLayout>
      <div className="max-w-6xl mx-auto py-4 sm:py-6">
        
        {/* Header */}
        <div className="mb-6 sm:mb-8">
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">Dashboard Overview</h1>
          <p className="mt-1 text-xs sm:text-sm text-slate-400">
            Welcome back! Here is a summary of your resume analysis performance and job matches.
          </p>
        </div>

        {/* Stats Cards Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 mb-6 sm:mb-8">
          
          {/* Resume Count Card */}
          <div className="relative rounded-2xl bg-slate-900/80 backdrop-blur-xl border border-slate-800/90 p-5 sm:p-6 shadow-[0_15px_35px_rgba(0,0,0,0.4)] hover:shadow-indigo-500/10 hover:border-indigo-500/30 transition-all duration-300 hover:-translate-y-1 overflow-hidden group">
            <div className="absolute -right-12 -bottom-12 w-36 h-36 bg-indigo-600/10 rounded-full blur-2xl group-hover:bg-indigo-600/20 transition-all"></div>
            
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Total Resumes</h3>
              <div className="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 flex items-center justify-center shadow-sm">
                <FaFilePdf className="text-lg" />
              </div>
            </div>
            
            <p className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">{resumes.length}</p>
            <p className="mt-2 text-xs text-slate-400 font-medium">
              {resumes.length === 1 ? '1 resume uploaded' : `${resumes.length} resumes uploaded`}
            </p>
          </div>

          {/* ATS Score Card */}
          <div className="relative rounded-2xl bg-slate-900/80 backdrop-blur-xl border border-slate-800/90 p-5 sm:p-6 shadow-[0_15px_35px_rgba(0,0,0,0.4)] hover:shadow-emerald-500/10 hover:border-emerald-500/30 transition-all duration-300 hover:-translate-y-1 overflow-hidden group">
            <div className="absolute -right-12 -bottom-12 w-36 h-36 bg-emerald-600/10 rounded-full blur-2xl group-hover:bg-emerald-600/20 transition-all"></div>
            
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Latest ATS Score</h3>
              <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 flex items-center justify-center shadow-sm">
                <FaTrophy className="text-lg" />
              </div>
            </div>

            {latestATSScore !== null ? (
              <>
                <div className="flex items-baseline gap-2">
                  <p className="text-3xl sm:text-4xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-emerald-400 to-teal-300">
                    {latestATSScore}
                  </p>
                  <span className="text-xs text-slate-500 font-medium">/ 100</span>
                </div>
                <div className="mt-2.5 flex items-center gap-2">
                  <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold border ${getScoreBgColor(latestATSScore)}`}>
                    <FaCheckCircle className="text-[10px]" />
                    {getScoreLabel(latestATSScore)}
                  </span>
                </div>
              </>
            ) : (
              <>
                <p className="text-3xl sm:text-4xl font-extrabold text-slate-600">-</p>
                <p className="mt-2 text-xs text-slate-500">No analysis completed yet</p>
              </>
            )}
          </div>

          {/* Job Matches Card */}
          <div className="relative rounded-2xl bg-slate-900/80 backdrop-blur-xl border border-slate-800/90 p-5 sm:p-6 shadow-[0_15px_35px_rgba(0,0,0,0.4)] hover:shadow-amber-500/10 hover:border-amber-500/30 transition-all duration-300 hover:-translate-y-1 overflow-hidden group sm:col-span-2 lg:col-span-1">
            <div className="absolute -right-12 -bottom-12 w-36 h-36 bg-amber-600/10 rounded-full blur-2xl group-hover:bg-amber-600/20 transition-all"></div>
            
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Job Matches</h3>
              <div className="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-400 flex items-center justify-center shadow-sm">
                <FaBriefcase className="text-lg" />
              </div>
            </div>

            <p className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">{jobMatches.length}</p>
            <p className="mt-2 text-xs text-amber-300/80 font-medium">
              {jobMatches.length > 0 ? `Best match rating: ${Math.round(bestMatchPercentage)}%` : 'No match recommendations yet'}
            </p>
          </div>

        </div>

        {/* Latest Resume Card */}
        {latestResume && (
          <div className="mb-6 sm:mb-8 bg-slate-900/80 backdrop-blur-xl border border-slate-800/90 rounded-2xl shadow-[0_20px_40px_rgba(0,0,0,0.4)] p-5 sm:p-6 group hover:border-slate-700 transition-all overflow-hidden">
            <div className="flex flex-wrap items-center justify-between gap-3 mb-4 pb-3 border-b border-slate-800/80">
              <h3 className="text-base sm:text-lg font-bold text-white tracking-tight">Latest Uploaded Resume</h3>
              <button
                onClick={() => navigate(`/resume/${latestResume.public_id}`)}
                className="text-indigo-400 hover:text-indigo-300 text-xs sm:text-sm font-semibold flex items-center gap-1.5 transition-all group-hover:translate-x-0.5 cursor-pointer"
              >
                <span>View Details</span>
                <FaArrowRight className="text-xs" />
              </button>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-12 h-12 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-center flex-shrink-0 shadow-inner group-hover:border-indigo-500/30 transition-all">
                {getFileIcon(latestResume.original_filename)}
              </div>
              <div className="flex-grow min-w-0">
                <h4 className="text-sm sm:text-base font-bold text-white truncate mb-1">
                  {formatFilename(latestResume.original_filename)}
                </h4>
                <div className="flex flex-wrap items-center gap-3 text-xs text-slate-400">
                  <span className="flex items-center gap-1.5">
                    <FaClock className="text-[11px] text-slate-500" />
                    <span>Uploaded: {new Date(latestResume.uploaded_at).toLocaleDateString()}</span>
                  </span>
                  <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full font-semibold border ${
                    latestResume.processing_status === 'completed' 
                      ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' 
                      : latestResume.processing_status === 'failed'
                      ? 'bg-rose-500/10 text-rose-400 border-rose-500/20'
                      : 'bg-amber-500/10 text-amber-400 border-amber-500/20'
                  }`}>
                    {latestResume.processing_status === 'completed' && <FaCheckCircle className="text-[10px]" />}
                    {latestResume.processing_status === 'failed' && <FaExclamationTriangle className="text-[10px]" />}
                    <span>{latestResume.processing_status.charAt(0).toUpperCase() + latestResume.processing_status.slice(1)}</span>
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Quick Actions Card */}
        <div className="bg-slate-900/80 backdrop-blur-xl border border-slate-800/90 rounded-2xl shadow-[0_20px_40px_rgba(0,0,0,0.4)] p-5 sm:p-6">
          <h3 className="text-base sm:text-lg font-bold text-white tracking-tight mb-4">Quick Actions</h3>
          
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3.5 sm:gap-4">
            
            <button
              onClick={() => navigate("/upload")}
              className="flex items-center justify-center gap-2.5 px-5 py-3.5 bg-gradient-to-r from-indigo-600 via-indigo-500 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-semibold text-xs sm:text-sm rounded-xl shadow-lg shadow-indigo-600/20 hover:shadow-indigo-500/35 hover:-translate-y-0.5 active:translate-y-0 transition-all duration-200 cursor-pointer"
            >
              <FaUpload className="text-xs" />
              <span>Upload Resume</span>
            </button>

            <button
              onClick={() => latestResume ? navigate(`/ats-score/${latestResume.public_id}`) : navigate("/my-resumes")}
              disabled={!latestResume}
              className="flex items-center justify-center gap-2.5 px-5 py-3.5 bg-gradient-to-r from-emerald-600 via-emerald-500 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-semibold text-xs sm:text-sm rounded-xl shadow-lg shadow-emerald-600/20 hover:shadow-emerald-500/35 hover:-translate-y-0.5 active:translate-y-0 transition-all duration-200 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-y-0 disabled:shadow-none"
            >
              <FaTrophy className="text-xs" />
              <span>View ATS Score</span>
            </button>

            <button
              onClick={() => latestResume ? navigate(`/jobs?resume=${latestResume.public_id}`) : navigate("/jobs")}
              disabled={resumes.length === 0}
              className="flex items-center justify-center gap-2.5 px-5 py-3.5 bg-gradient-to-r from-amber-600 via-amber-500 to-orange-600 hover:from-amber-500 hover:to-orange-500 text-white font-semibold text-xs sm:text-sm rounded-xl shadow-lg shadow-amber-600/20 hover:shadow-amber-500/35 hover:-translate-y-0.5 active:translate-y-0 transition-all duration-200 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-y-0 disabled:shadow-none"
            >
              <FaBriefcase className="text-xs" />
              <span>Find Matching Jobs</span>
            </button>

          </div>
        </div>

        {/* Empty State Card */}
        {resumes.length === 0 && (
          <div className="mt-6 rounded-2xl border border-slate-800/90 bg-slate-900/80 backdrop-blur-xl p-8 sm:p-12 text-center shadow-[0_20px_40px_rgba(0,0,0,0.4)]">
            <div className="w-12 h-12 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 flex items-center justify-center mx-auto mb-4">
              <FaFilePdf className="text-xl" />
            </div>
            <h3 className="text-base sm:text-lg font-bold text-white mb-1.5">No Resumes Uploaded Yet</h3>
            <p className="text-slate-400 text-xs sm:text-sm max-w-md mx-auto mb-6">
              Upload your first resume to generate automated ATS scores, keyword match diagnostics, and tailored job recommendations.
            </p>
            <button
              onClick={() => navigate("/upload")}
              className="px-5 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-semibold text-xs sm:text-sm rounded-xl shadow-lg shadow-indigo-600/25 hover:shadow-indigo-500/40 transition-all flex items-center gap-2 mx-auto cursor-pointer"
            >
              <FaUpload className="text-xs" />
              <span>Upload Resume Now</span>
            </button>
          </div>
        )}

      </div>
    </DashboardLayout>
  );
}

export default Dashboard;

