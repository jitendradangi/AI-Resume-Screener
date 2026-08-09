import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import DashboardLayout from "../layouts/DashboardLayout";
import {
  FaFilePdf,
  FaFileWord,
  FaArrowLeft,
  FaCheckCircle,
  FaExclamationCircle,
  FaLightbulb,
} from "react-icons/fa";

import { FaBrain } from "react-icons/fa6";
import { getResumeDetails, analyzeResume } from "../services/resumeService";

const getFileIcon = (filename) => {
  const extension = filename.split(".").pop().toLowerCase();

  switch (extension) {
    case "pdf":
      return <FaFilePdf color="#e53935" size={32} />;

    case "doc":
    case "docx":
      return <FaFileWord color="#1565c0" size={32} />;

    default:
      return null;
  }
};

const formatFilename = (filename) => {
  if (!filename) return "";
  const parts = filename.split('_');
  if (parts.length > 1 && parts[0].length === 36) {
    return parts.slice(1).join('_');
  }
  return filename;
};

const formatFileSize = (bytes) => {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + " " + sizes[i];
};

function ResumeDetails() {
  const { public_id } = useParams();
  const navigate = useNavigate();
  const [resume, setResume] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisError, setAnalysisError] = useState("");

  useEffect(() => {
    const fetchResumeDetails = async () => {
      try {
        const data = await getResumeDetails(public_id);
        setResume(data);
      } catch (err) {
        setError("Failed to load resume details");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchResumeDetails();
  }, [public_id]);

  const handleAnalyze = async () => {
    try {
      setAnalyzing(true);
      setAnalysisError("");
      const result = await analyzeResume(public_id);
      // Store the analysis result in sessionStorage for the ATS Score page
      sessionStorage.setItem(`analysis_${public_id}`, JSON.stringify(result));
      // Navigate to ATS Score page with the analysis data
      navigate(`/ats-score/${public_id}`);
    } catch (err) {
      setAnalysisError("Failed to analyze resume. Please try again.");
      console.error(err);
    } finally {
      setAnalyzing(false);
    }
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="max-w-4xl mx-auto py-8">
          <h3 className="text-lg font-medium text-slate-900 dark:text-white">Loading...</h3>
        </div>
      </DashboardLayout>
    );
  }

  if (error || !resume) {
    return (
      <DashboardLayout>
        <div className="max-w-4xl mx-auto py-8">
          <div className="bg-rose-50 dark:bg-rose-900/30 border border-rose-200 dark:border-rose-900/50 rounded-lg p-6">
            <p className="text-rose-700 dark:text-rose-400 font-medium">{error || "Resume not found"}</p>
            <button
              onClick={() => navigate("/my-resumes")}
              className="mt-4 text-indigo-600 dark:text-indigo-400 hover:text-indigo-700 dark:hover:text-indigo-300 font-medium"
            >
              Back to My Resumes
            </button>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="max-w-4xl mx-auto py-8">
        {/* Back Button */}
        <button
          onClick={() => navigate("/my-resumes")}
          className="mb-6 flex items-center gap-2 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 transition-colors"
        >
          <FaArrowLeft size={16} />
          <span className="font-medium">Back to My Resumes</span>
        </button>

        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Resume Details</h1>
          <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">
            View and analyze your uploaded resume
          </p>
        </div>

        {/* Resume Info Card */}
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm p-6 mb-6">
          <div className="flex items-start gap-6">
            <div className="flex-shrink-0">
              {getFileIcon(resume.original_filename)}
            </div>
            <div className="flex-grow">
              <h2 className="text-xl font-semibold text-slate-900 dark:text-white mb-2">
                {formatFilename(resume.original_filename)}
              </h2>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-slate-500 dark:text-slate-400">File Size:</span>
                  <span className="ml-2 text-slate-900 dark:text-slate-200">{formatFileSize(resume.filesize)}</span>
                </div>
                <div>
                  <span className="text-slate-500 dark:text-slate-400">Uploaded:</span>
                  <span className="ml-2 text-slate-900 dark:text-slate-200">
                    {new Date(resume.uploaded_at).toLocaleDateString()}
                  </span>
                </div>
                <div>
                  <span className="text-slate-500 dark:text-slate-400">Status:</span>
                  <span className={`ml-2 font-medium ${
                    resume.processing_status === 'completed' 
                      ? 'text-emerald-600 dark:text-emerald-400' 
                      : resume.processing_status === 'failed'
                      ? 'text-rose-600 dark:text-rose-400'
                      : 'text-amber-600 dark:text-amber-400'
                  }`}>
                    {resume.processing_status.charAt(0).toUpperCase() + resume.processing_status.slice(1)}
                  </span>
                </div>
                <div>
                  <span className="text-slate-500 dark:text-slate-400">Last Updated:</span>
                  <span className="ml-2 text-slate-900 dark:text-slate-200">
                    {new Date(resume.updated_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
              {resume.processing_error && (
                <div className="mt-4 p-3 bg-rose-50 dark:bg-rose-900/30 border border-rose-200 dark:border-rose-900/50 rounded-lg">
                  <p className="text-sm text-rose-700 dark:text-rose-400">
                    <span className="font-medium">Error:</span> {resume.processing_error}
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm p-6">
          <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-4">Actions</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            <button
              className="flex items-center justify-center gap-2 px-4 py-3 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              onClick={handleAnalyze}
              disabled={analyzing}
            >
              <FaBrain />
              <span>{analyzing ? "Analyzing..." : "Get ATS Score"}</span>
            </button>
            <button
              className="flex items-center justify-center gap-2 px-4 py-3 bg-emerald-600 text-white font-medium rounded-lg hover:bg-emerald-700 transition-colors"
              onClick={() => navigate(`/jobs?resume=${public_id}`)}
            >
              <span>Find Jobs</span>
            </button>
            <button
              className="flex items-center justify-center gap-2 px-4 py-3 bg-slate-600 text-white font-medium rounded-lg hover:bg-slate-700 transition-colors"
              onClick={() => navigate("/upload")}
            >
              <span>Upload New Resume</span>
            </button>
          </div>
          {analysisError && (
            <div className="mt-4 p-3 bg-rose-50 dark:bg-rose-900/30 border border-rose-200 dark:border-rose-900/50 rounded-lg">
              <p className="text-sm text-rose-700 dark:text-rose-400">{analysisError}</p>
            </div>
          )}
        </div>

        {/* Info Section */}
        <div className="mt-6 bg-blue-50 dark:bg-blue-900/30 border border-blue-200 dark:border-blue-900/50 rounded-lg p-4">
          <p className="text-sm text-blue-700 dark:text-blue-400">
            <span className="font-medium">Tip:</span> Use the actions above to analyze your resume with AI, get an ATS score, or find matching jobs.
          </p>
        </div>
      </div>
    </DashboardLayout>
  );
}

export default ResumeDetails;
