import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import DashboardLayout from "../layouts/DashboardLayout";
import { FaBriefcase, FaArrowLeft, FaTrophy, FaCheckCircle, FaTimesCircle, FaSpinner } from "react-icons/fa";
import { getMyResumes } from "../services/resumeService";
import { getJobRecommendations } from "../services/jobService";

function Jobs() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [resumes, setResumes] = useState([]);
  const [selectedResume, setSelectedResume] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [generatingMatches, setGeneratingMatches] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchResumes = async () => {
      try {
        const data = await getMyResumes();
        setResumes(data);
        
        // Check if a resume is specified in the URL
        const resumeParam = searchParams.get('resume');
        if (resumeParam && data.some(r => r.public_id === resumeParam)) {
          setSelectedResume(resumeParam);
        } else if (data.length > 0) {
          setSelectedResume(data[0].public_id);
        }
      } catch (err) {
        setError("Failed to load resumes");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchResumes();
  }, [searchParams]);

  useEffect(() => {
    if (selectedResume) {
      fetchRecommendations(selectedResume);
    }
  }, [selectedResume]);

  const fetchRecommendations = async (resumeId) => {
    try {
      setGeneratingMatches(true);
      setError("");
      const data = await getJobRecommendations(resumeId, 10, 50);
      setRecommendations(data);
    } catch (err) {
      setError("Failed to load job recommendations");
      console.error(err);
    } finally {
      setGeneratingMatches(false);
    }
  };

  const handleResumeChange = (e) => {
    setSelectedResume(e.target.value);
  };

  const handleViewMatch = async (jobPublicId) => {
    if (selectedResume) {
      navigate(`/match/${selectedResume}/${jobPublicId}`);
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

  if (loading) {
    return (
      <DashboardLayout>
        <div className="max-w-6xl mx-auto py-8">
          <h3 className="text-lg font-medium text-slate-900 dark:text-white">Loading...</h3>
        </div>
      </DashboardLayout>
    );
  }

  if (resumes.length === 0) {
    return (
      <DashboardLayout>
        <div className="max-w-6xl mx-auto py-8">
          <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-12 text-center shadow-sm">
            <h3 className="text-lg font-medium text-slate-900 dark:text-white">No Resumes Found</h3>
            <p className="mt-2 text-slate-500 dark:text-slate-400">Upload a resume to start getting job recommendations.</p>
            <button
              onClick={() => navigate("/upload")}
              className="mt-4 px-6 py-3 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 transition-colors"
            >
              Upload Resume
            </button>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="max-w-6xl mx-auto py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Job Matches</h1>
          <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">Find jobs tailored to your resume</p>
        </div>

        {/* Resume Selector */}
        <div className="mb-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm p-6">
          <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
            Select Resume
          </label>
          <select
            value={selectedResume || ""}
            onChange={handleResumeChange}
            className="w-full px-4 py-2 border border-slate-300 dark:border-slate-700 rounded-lg bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          >
            {resumes.map((resume) => (
              <option key={resume.public_id} value={resume.public_id}>
                {resume.original_filename}
              </option>
            ))}
          </select>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 bg-rose-50 dark:bg-rose-900/30 border border-rose-200 dark:border-rose-900/50 rounded-lg p-4">
            <p className="text-sm text-rose-700 dark:text-rose-400">{error}</p>
          </div>
        )}

        {/* Loading State */}
        {generatingMatches && (
          <div className="mb-6 flex items-center justify-center gap-2 text-slate-600 dark:text-slate-400">
            <FaSpinner className="animate-spin" />
            <span>Finding matching jobs...</span>
          </div>
        )}

        {/* Jobs Grid */}
        {recommendations.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {recommendations.map((job) => (
              <div
                key={job.job_public_id}
                className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm hover:shadow-md transition-shadow cursor-pointer"
                onClick={() => handleViewMatch(job.job_public_id)}
              >
                {/* Job Card Header */}
                <div className="p-6 border-b border-slate-200 dark:border-slate-800">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-grow">
                      <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-1">
                        {job.title}
                      </h3>
                      <p className="text-sm text-slate-600 dark:text-slate-400">
                        {job.company}
                      </p>
                      {job.location && (
                        <p className="text-xs text-slate-500 dark:text-slate-500 mt-1">
                          {job.location}
                        </p>
                      )}
                    </div>
                    <div className={`px-3 py-1 rounded-full text-sm font-medium ${getMatchColor(job.overall_match)}`}>
                      {Math.round(job.overall_match)}%
                    </div>
                  </div>
                </div>

                {/* Match Details */}
                <div className="p-6">
                  <div className="mb-4">
                    <p className="text-xs text-slate-500 dark:text-slate-400 mb-2">Match Level</p>
                    <span className={`px-2 py-1 rounded text-xs font-medium ${getMatchColor(job.overall_match)}`}>
                      {job.match_level}
                    </span>
                  </div>

                  {/* Skills */}
                  <div className="mb-4">
                    <p className="text-xs text-slate-500 dark:text-slate-400 mb-2">Skills</p>
                    <div className="flex flex-wrap gap-2">
                      {job.matched_skills.slice(0, 4).map((skill, index) => (
                        <span
                          key={index}
                          className="flex items-center gap-1 text-xs text-emerald-600 dark:text-emerald-400"
                        >
                          <FaCheckCircle size={12} />
                          {skill}
                        </span>
                      ))}
                      {job.missing_skills.length > 0 && (
                        <span className="flex items-center gap-1 text-xs text-rose-600 dark:text-rose-400">
                          <FaTimesCircle size={12} />
                          +{job.missing_skills.length} more
                        </span>
                      )}
                    </div>
                  </div>

                  {/* Component Scores */}
                  <div className="mb-4">
                    <p className="text-xs text-slate-500 dark:text-slate-400 mb-2">Component Scores</p>
                    <div className="grid grid-cols-2 gap-2 text-xs">
                      <div className="flex justify-between">
                        <span className="text-slate-600 dark:text-slate-400">Skills:</span>
                        <span className="font-medium text-slate-900 dark:text-white">{job.component_scores.skills || 0}%</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-600 dark:text-slate-400">Experience:</span>
                        <span className="font-medium text-slate-900 dark:text-white">{job.component_scores.experience || 0}%</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-600 dark:text-slate-400">Education:</span>
                        <span className="font-medium text-slate-900 dark:text-white">{job.component_scores.education || 0}%</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-slate-600 dark:text-slate-400">Projects:</span>
                        <span className="font-medium text-slate-900 dark:text-white">{job.component_scores.projects || 0}%</span>
                      </div>
                    </div>
                  </div>

                  {/* View Match Button */}
                  <button className="w-full mt-4 px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-lg hover:bg-indigo-700 transition-colors flex items-center justify-center gap-2">
                    <FaTrophy />
                    View Match Details
                  </button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          !generatingMatches && (
            <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-12 text-center shadow-sm">
              <h3 className="text-lg font-medium text-slate-900 dark:text-white">No Matching Jobs Found</h3>
              <p className="mt-2 text-slate-500 dark:text-slate-400">
                Try improving your resume or upload a different one to see more job recommendations.
              </p>
            </div>
          )
        )}
      </div>
    </DashboardLayout>
  );
}

export default Jobs;
