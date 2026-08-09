import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import DashboardLayout from "../layouts/DashboardLayout";
import { FaArrowLeft, FaCheckCircle, FaTimesCircle, FaTrophy, FaBrain, FaBullseye, FaGraduationCap, FaProjectDiagram, FaBriefcase, FaSpinner } from "react-icons/fa";
import { getMatch, generateMatch } from "../services/jobService";

function MatchDetails() {
  const { resumePublicId, jobPublicId } = useParams();
  const navigate = useNavigate();
  const [match, setMatch] = useState(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchMatch = async () => {
      try {
        setLoading(true);
        setError("");
        const data = await getMatch(resumePublicId, jobPublicId);
        setMatch(data);
      } catch (err) {
        setError("Failed to load match details");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchMatch();
  }, [resumePublicId, jobPublicId]);

  const handleGenerateMatch = async () => {
    try {
      setGenerating(true);
      setError("");
      const data = await generateMatch(resumePublicId, jobPublicId);
      setMatch(data);
    } catch (err) {
      setError("Failed to generate comprehensive match");
      console.error(err);
    } finally {
      setGenerating(false);
    }
  };

  const getMatchColor = (score) => {
    if (score >= 80) return "text-emerald-600 dark:text-emerald-400 bg-emerald-100 dark:bg-emerald-900/30 border-emerald-200 dark:border-emerald-900/50";
    if (score >= 60) return "text-amber-600 dark:text-amber-400 bg-amber-100 dark:bg-amber-900/30 border-amber-200 dark:border-amber-900/50";
    return "text-rose-600 dark:text-rose-400 bg-rose-100 dark:bg-rose-900/30 border-rose-200 dark:border-rose-900/50";
  };

  const getMatchLabel = (score) => {
    if (score >= 80) return "Excellent Match";
    if (score >= 60) return "Good Match";
    if (score >= 40) return "Fair Match";
    return "Poor Match";
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
          <h3 className="text-lg font-medium text-slate-900 dark:text-white">Loading match details...</h3>
        </div>
      </DashboardLayout>
    );
  }

  if (error && !match) {
    return (
      <DashboardLayout>
        <div className="max-w-6xl mx-auto py-8">
          <div className="bg-rose-50 dark:bg-rose-900/30 border border-rose-200 dark:border-rose-900/50 rounded-lg p-6">
            <p className="text-rose-700 dark:text-rose-400 font-medium">{error}</p>
            <button
              onClick={() => navigate("/jobs")}
              className="mt-4 text-indigo-600 dark:text-indigo-400 hover:text-indigo-700 dark:hover:text-indigo-300 font-medium"
            >
              Back to Jobs
            </button>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="max-w-6xl mx-auto py-8">
        {/* Back Button */}
        <button
          onClick={() => navigate("/jobs")}
          className="mb-6 flex items-center gap-2 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 transition-colors"
        >
          <FaArrowLeft size={16} />
          <span className="font-medium">Back to Jobs</span>
        </button>

        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Match Details</h1>
          <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">
            Detailed analysis of your resume's compatibility with this job
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 bg-rose-50 dark:bg-rose-900/30 border border-rose-200 dark:border-rose-900/50 rounded-lg p-4">
            <p className="text-sm text-rose-700 dark:text-rose-400">{error}</p>
          </div>
        )}

        {/* Generate Match Button if no match exists */}
        {!match && (
          <div className="mb-8 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm p-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-slate-900 dark:text-white">No Match Available</h3>
                <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
                  Generate a comprehensive match analysis including skills, experience, education, projects, and semantic matching
                </p>
              </div>
              <button
                onClick={handleGenerateMatch}
                disabled={generating}
                className="px-6 py-3 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                {generating ? <FaSpinner className="animate-spin" /> : <FaBrain />}
                <span>{generating ? "Generating..." : "Generate Match"}</span>
              </button>
            </div>
          </div>
        )}

        {match && (
          <>
            {/* Overall Match Score */}
            <div className={`mb-8 p-8 rounded-xl border-2 ${getMatchColor(match.match_score)}`}>
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-slate-600 dark:text-slate-400 mb-2">Overall Match Score</p>
                  <div className="flex items-baseline gap-3">
                    <p className={`text-6xl font-bold ${getMatchColor(match.match_score)}`}>
                      {match.match_score}
                    </p>
                    <span className="text-2xl text-slate-600 dark:text-slate-400">/100</span>
                  </div>
                  <div className="mt-2">
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${getMatchColor(match.match_score)}`}>
                      {getMatchLabel(match.match_score)}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Recommendation */}
            {match.recommendation && (
              <div className="mb-8 bg-gradient-to-r from-indigo-50 to-purple-50 dark:from-indigo-900/30 dark:to-purple-900/30 border border-indigo-200 dark:border-indigo-900/50 rounded-xl shadow-sm p-6">
                <h2 className="text-xl font-semibold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
                  <FaTrophy className="text-indigo-600" />
                  Recommendation
                </h2>
                <p className="text-slate-700 dark:text-slate-300 text-base leading-relaxed">
                  {match.recommendation}
                </p>
              </div>
            )}

            {/* Skills Analysis */}
            <div className="mb-8 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm p-6">
              <h2 className="text-xl font-semibold text-slate-900 dark:text-white mb-6 flex items-center gap-2">
                <FaBriefcase className="text-indigo-600" />
                Skills Analysis
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Matched Skills */}
                <div>
                  <p className="text-sm font-medium text-slate-700 dark:text-slate-300 mb-3">Matched Skills</p>
                  <div className="flex flex-wrap gap-2">
                    {match.skills.matched.length > 0 ? (
                      match.skills.matched.map((skill, index) => (
                        <span
                          key={index}
                          className="flex items-center gap-2 px-3 py-2 bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300 rounded-full text-sm font-medium border border-emerald-200 dark:border-emerald-900/50"
                        >
                          <FaCheckCircle size={14} />
                          {skill}
                        </span>
                      ))
                    ) : (
                      <p className="text-sm text-slate-500 dark:text-slate-400">No matched skills</p>
                    )}
                  </div>
                </div>

                {/* Missing Skills */}
                <div>
                  <p className="text-sm font-medium text-slate-700 dark:text-slate-300 mb-3">Missing Skills</p>
                  <div className="flex flex-wrap gap-2">
                    {match.skills.missing.length > 0 ? (
                      match.skills.missing.map((skill, index) => (
                        <span
                          key={index}
                          className="flex items-center gap-2 px-3 py-2 bg-rose-100 dark:bg-rose-900/30 text-rose-700 dark:text-rose-300 rounded-full text-sm font-medium border border-rose-200 dark:border-rose-900/50"
                        >
                          <FaTimesCircle size={14} />
                          {skill}
                        </span>
                      ))
                    ) : (
                      <p className="text-sm text-slate-500 dark:text-slate-400">No missing skills</p>
                    )}
                  </div>
                </div>
              </div>
            </div>

            {/* Component Scores */}
            <div className="mb-8 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm p-6">
              <h2 className="text-xl font-semibold text-slate-900 dark:text-white mb-6">Component Scores</h2>
              <div className="space-y-4">
                {/* Skills */}
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium text-slate-700 dark:text-slate-300 flex items-center gap-2">
                      <FaBriefcase className="text-indigo-600" />
                      Skills Match
                    </span>
                    <span className="text-sm font-semibold text-slate-900 dark:text-white">
                      {match.component_scores?.skills || 0}%
                    </span>
                  </div>
                  <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-3">
                    <div
                      className={`h-3 rounded-full transition-all duration-500 ${getProgressColor(match.component_scores?.skills || 0)}`}
                      style={{ width: `${match.component_scores?.skills || 0}%` }}
                    />
                  </div>
                </div>

                {/* Experience */}
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium text-slate-700 dark:text-slate-300 flex items-center gap-2">
                      <FaBriefcase className="text-indigo-600" />
                      Experience Match
                    </span>
                    <span className="text-sm font-semibold text-slate-900 dark:text-white">
                      {match.component_scores?.experience || 0}%
                    </span>
                  </div>
                  <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-3">
                    <div
                      className={`h-3 rounded-full transition-all duration-500 ${getProgressColor(match.component_scores?.experience || 0)}`}
                      style={{ width: `${match.component_scores?.experience || 0}%` }}
                    />
                  </div>
                </div>

                {/* Education */}
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium text-slate-700 dark:text-slate-300 flex items-center gap-2">
                      <FaGraduationCap className="text-indigo-600" />
                      Education Match
                    </span>
                    <span className="text-sm font-semibold text-slate-900 dark:text-white">
                      {match.component_scores?.education || 0}%
                    </span>
                  </div>
                  <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-3">
                    <div
                      className={`h-3 rounded-full transition-all duration-500 ${getProgressColor(match.component_scores?.education || 0)}`}
                      style={{ width: `${match.component_scores?.education || 0}%` }}
                    />
                  </div>
                </div>

                {/* Projects */}
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium text-slate-700 dark:text-slate-300 flex items-center gap-2">
                      <FaProjectDiagram className="text-indigo-600" />
                      Project Match
                    </span>
                    <span className="text-sm font-semibold text-slate-900 dark:text-white">
                      {match.component_scores?.projects || 0}%
                    </span>
                  </div>
                  <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-3">
                    <div
                      className={`h-3 rounded-full transition-all duration-500 ${getProgressColor(match.component_scores?.projects || 0)}`}
                      style={{ width: `${match.component_scores?.projects || 0}%` }}
                    />
                  </div>
                </div>

                {/* Semantic */}
                <div>
                  <div className="flex justify-between mb-2">
                    <span className="text-sm font-medium text-slate-700 dark:text-slate-300 flex items-center gap-2">
                      <FaBullseye className="text-indigo-600" />
                      AI/Semantic Match
                    </span>
                    <span className="text-sm font-semibold text-slate-900 dark:text-white">
                      {match.component_scores?.semantic || 0}%
                    </span>
                  </div>
                  <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-3">
                    <div
                      className={`h-3 rounded-full transition-all duration-500 ${getProgressColor(match.component_scores?.semantic || 0)}`}
                      style={{ width: `${match.component_scores?.semantic || 0}%` }}
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-4">
              <button
                onClick={() => navigate("/jobs")}
                className="px-6 py-3 bg-emerald-600 text-white font-medium rounded-lg hover:bg-emerald-700 transition-colors"
              >
                View Other Jobs
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

export default MatchDetails;
