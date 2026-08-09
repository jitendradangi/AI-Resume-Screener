import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import DashboardLayout from "../layouts/DashboardLayout";
import { FaArrowLeft, FaCheckCircle, FaExclamationCircle, FaLightbulb, FaTrophy, FaRegChartBar } from "react-icons/fa";
import { getResumeDetails, analyzeResume } from "../services/resumeService";

const formatFilename = (filename) => {
  if (!filename) return "";
  const parts = filename.split('_');
  if (parts.length > 1 && parts[0].length === 36) {
    return parts.slice(1).join('_');
  }
  return filename;
};

function ATSScore() {
  const { public_id } = useParams();
  const navigate = useNavigate();
  const [resume, setResume] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [isFreshAnalysis, setIsFreshAnalysis] = useState(false);

  useEffect(() => {
    if (!public_id) {
      setError("No resume ID provided");
      setLoading(false);
      return;
    }

    const fetchResumeDetails = async () => {
      try {
        const data = await getResumeDetails(public_id);
        setResume(data);
        
        // First check sessionStorage for fresh analysis (from "Get ATS Score" button)
        const freshAnalysis = sessionStorage.getItem(`analysis_${public_id}`);
        if (freshAnalysis) {
          setAnalysis(JSON.parse(freshAnalysis));
          setIsFreshAnalysis(true);
          // Clear sessionStorage after loading
          sessionStorage.removeItem(`analysis_${public_id}`);
        } 
        // Then check if analysis already exists in the backend
        else if (data.ai_analysis) {
          setAnalysis(data.ai_analysis);
          setIsFreshAnalysis(false);
        }
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
      setError("");
      const result = await analyzeResume(public_id);
      setAnalysis(result);
    } catch (err) {
      setError("Failed to analyze resume. Please try again.");
      console.error(err);
    } finally {
      setAnalyzing(false);
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
    return "Needs Improvement";
  };

  const getProgressColor = (percentage) => {
    if (percentage >= 80) return "bg-emerald-500";
    if (percentage >= 60) return "bg-amber-500";
    return "bg-rose-500";
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="max-w-6xl mx-auto py-8">
          <h3 className="text-lg font-medium text-slate-900 dark:text-white">Loading...</h3>
        </div>
      </DashboardLayout>
    );
  }

  if (error || !resume) {
    return (
      <DashboardLayout>
        <div className="max-w-6xl mx-auto py-8">
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

  const overallScore = analysis?.overall_score || 0;
  const scoreBreakdown = analysis?.score_breakdown || {};
  
  // Map backend score breakdown to frontend display names
  const displayScores = {
    content_quality: { name: "Content Quality", value: scoreBreakdown.content_quality || 0, max: 25 },
    skills_relevance: { name: "Skills Relevance", value: scoreBreakdown.skills_relevance || 0, max: 25 },
    experience_depth: { name: "Experience Depth", value: scoreBreakdown.experience_depth || 0, max: 25 },
    formatting_clarity: { name: "Formatting Clarity", value: scoreBreakdown.formatting_clarity || 0, max: 25 },
  };

  return (
    <DashboardLayout>
      <div className="max-w-6xl mx-auto py-8">
        {/* Back Button */}
        <button
          onClick={() => public_id ? navigate(`/resume/${public_id}`) : navigate("/my-resumes")}
          className="mb-6 flex items-center gap-2 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 transition-colors"
        >
          <FaArrowLeft size={16} />
          <span className="font-medium">{public_id ? "Back to Resume Details" : "Back to My Resumes"}</span>
        </button>

        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-900 dark:text-white">ATS Score Analysis</h1>
          <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">
            Comprehensive analysis of your resume's ATS compatibility
          </p>
        </div>

        {/* Resume Information Card */}
        {resume && (
          <div className="mb-8 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm p-6">
            <h2 className="text-lg font-semibold text-slate-900 dark:text-white mb-4">Resume Information</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div>
                <p className="text-xs text-slate-500 dark:text-slate-400 mb-1">Resume Name</p>
                <p className="text-sm font-medium text-slate-900 dark:text-white truncate">
                  {formatFilename(resume.original_filename)}
                </p>
              </div>
              <div>
                <p className="text-xs text-slate-500 dark:text-slate-400 mb-1">Uploaded Date</p>
                <p className="text-sm font-medium text-slate-900 dark:text-white">
                  {new Date(resume.uploaded_at).toLocaleDateString()}
                </p>
              </div>
              <div>
                <p className="text-xs text-slate-500 dark:text-slate-400 mb-1">File Size</p>
                <p className="text-sm font-medium text-slate-900 dark:text-white">
                  {(resume.filesize / 1024).toFixed(2)} KB
                </p>
              </div>
              <div>
                <p className="text-xs text-slate-500 dark:text-slate-400 mb-1">Analysis Time</p>
                <p className="text-sm font-medium text-slate-900 dark:text-white">
                  {isFreshAnalysis ? 'Just now' : (analysis ? new Date(resume.updated_at).toLocaleString() : 'Not analyzed')}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Analyze Button if no analysis exists */}
        {!analysis && public_id && (
          <div className="mb-8 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm p-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-slate-900 dark:text-white">No Analysis Available</h3>
                <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
                  Get your ATS score to see detailed analysis and recommendations
                </p>
              </div>
              <button
                onClick={handleAnalyze}
                disabled={analyzing}
                className="px-6 py-3 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                <FaTrophy />
                <span>{analyzing ? "Analyzing..." : "Get ATS Score"}</span>
              </button>
            </div>
            {error && (
              <div className="mt-4 p-3 bg-rose-50 dark:bg-rose-900/30 border border-rose-200 dark:border-rose-900/50 rounded-lg">
                <p className="text-sm text-rose-700 dark:text-rose-400">{error}</p>
              </div>
            )}
          </div>
        )}

        {!public_id && (
          <div className="mb-8 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm p-6">
            <div className="text-center">
              <h3 className="text-lg font-semibold text-slate-900 dark:text-white">No Resume Selected</h3>
              <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">
                Please select a resume from My Resumes to view its ATS score
              </p>
              <button
                onClick={() => navigate("/my-resumes")}
                className="mt-4 px-6 py-3 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 transition-colors"
              >
                Go to My Resumes
              </button>
            </div>
          </div>
        )}

        {analysis && (
          <>
            {/* Section 1: Overall ATS Score */}
            <div className={`mb-8 p-8 rounded-xl border-2 ${getScoreBgColor(overallScore)}`}>
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-slate-600 dark:text-slate-400 mb-2">Overall ATS Score</p>
                  <div className="flex items-baseline gap-3">
                    <p className={`text-6xl font-bold ${getScoreColor(overallScore)}`}>
                      {overallScore}
                    </p>
                    <span className="text-2xl text-slate-600 dark:text-slate-400">/100</span>
                  </div>
                  <div className="mt-2 flex items-center gap-2">
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${getScoreBgColor(overallScore)} ${getScoreColor(overallScore)}`}>
                      {getScoreLabel(overallScore)}
                    </span>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm text-slate-600 dark:text-slate-400 mb-1">Experience Level</p>
                  <p className="text-xl font-semibold text-slate-900 dark:text-white">
                    {analysis.experience_level || "Not determined"}
                  </p>
                </div>
              </div>
            </div>

            {/* Section 2: Section-wise Scores */}
            <div className="mb-8 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm p-6">
              <h2 className="text-xl font-semibold text-slate-900 dark:text-white mb-6 flex items-center gap-2">
                <FaRegChartBar className="text-indigo-600" />
                Section-wise Scores
              </h2>
              <div className="space-y-6">
                {Object.entries(displayScores).map(([key, score]) => (
                  <div key={key}>
                    <div className="flex justify-between mb-2">
                      <span className="text-sm font-medium text-slate-700 dark:text-slate-300">{score.name}</span>
                      <span className="text-sm font-semibold text-slate-900 dark:text-white">{score.value}/{score.max}</span>
                    </div>
                    <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-3">
                      <div
                        className={`h-3 rounded-full transition-all duration-500 ${getProgressColor((score.value / score.max) * 100)}`}
                        style={{ width: `${(score.value / score.max) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Section 3: Strengths */}
            {analysis.strengths && analysis.strengths.length > 0 && (
              <div className="mb-8 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm p-6">
                <h2 className="text-xl font-semibold text-slate-900 dark:text-white mb-6 flex items-center gap-2">
                  <FaCheckCircle className="text-emerald-600" />
                  Strengths
                </h2>
                <ul className="space-y-3">
                  {analysis.strengths.map((strength, index) => (
                    <li key={index} className="flex items-start gap-3 text-slate-700 dark:text-slate-300">
                      <span className="text-emerald-600 mt-1 text-lg">✓</span>
                      <span className="text-base">{strength}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Section 4: Areas for Improvement */}
            {analysis.weaknesses && analysis.weaknesses.length > 0 && (
              <div className="mb-8 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm p-6">
                <h2 className="text-xl font-semibold text-slate-900 dark:text-white mb-6 flex items-center gap-2">
                  <FaExclamationCircle className="text-amber-600" />
                  Areas for Improvement
                </h2>
                <ul className="space-y-3">
                  {analysis.weaknesses.map((weakness, index) => (
                    <li key={index} className="flex items-start gap-3 text-slate-700 dark:text-slate-300">
                      <span className="text-amber-600 mt-1 text-lg">!</span>
                      <span className="text-base">{weakness}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Section 5: Missing Skills */}
            {analysis.missing_skills && analysis.missing_skills.length > 0 && (
              <div className="mb-8 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm p-6">
                <h2 className="text-xl font-semibold text-slate-900 dark:text-white mb-6">Missing Skills</h2>
                <div className="flex flex-wrap gap-3">
                  {analysis.missing_skills.map((skill, index) => (
                    <span
                      key={index}
                      className="px-4 py-2 bg-rose-100 dark:bg-rose-900/30 text-rose-700 dark:text-rose-300 rounded-full text-sm font-medium border border-rose-200 dark:border-rose-900/50"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Section 6: AI Suggestions */}
            {analysis.recommendations && analysis.recommendations.length > 0 && (
              <div className="mb-8 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm p-6">
                <h2 className="text-xl font-semibold text-slate-900 dark:text-white mb-6 flex items-center gap-2">
                  <FaLightbulb className="text-amber-500" />
                  AI Suggestions
                </h2>
                <ul className="space-y-3">
                  {analysis.recommendations.map((recommendation, index) => (
                    <li key={index} className="flex items-start gap-3 text-slate-700 dark:text-slate-300">
                      <span className="text-amber-500 mt-1 text-lg">💡</span>
                      <span className="text-base">{recommendation}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Section 7: AI Recommendation Summary */}
            {analysis.summary && (
              <div className="mb-8 bg-gradient-to-r from-indigo-50 to-purple-50 dark:from-indigo-900/30 dark:to-purple-900/30 border border-indigo-200 dark:border-indigo-900/50 rounded-xl shadow-sm p-6">
                <h2 className="text-xl font-semibold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
                  <FaTrophy className="text-indigo-600" />
                  AI Recommendation
                </h2>
                <p className="text-slate-700 dark:text-slate-300 text-base leading-relaxed">
                  {analysis.summary}
                </p>
              </div>
            )}

            {/* Top Skills */}
            {analysis.top_skills && analysis.top_skills.length > 0 && (
              <div className="mb-8 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm p-6">
                <h2 className="text-xl font-semibold text-slate-900 dark:text-white mb-4">Top Skills</h2>
                <div className="flex flex-wrap gap-3">
                  {analysis.top_skills.map((skill, index) => (
                    <span
                      key={index}
                      className="px-4 py-2 bg-indigo-100 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300 rounded-full text-sm font-medium border border-indigo-200 dark:border-indigo-900/50"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex gap-4">
              <button
                onClick={() => navigate("/jobs")}
                className="px-6 py-3 bg-emerald-600 text-white font-medium rounded-lg hover:bg-emerald-700 transition-colors"
              >
                Find Matching Jobs
              </button>
              <button
                onClick={() => navigate("/upload")}
                className="px-6 py-3 bg-slate-600 text-white font-medium rounded-lg hover:bg-slate-700 transition-colors"
              >
                Upload New Resume
              </button>
            </div>
          </>
        )}
      </div>
    </DashboardLayout>
  );
}

export default ATSScore;
