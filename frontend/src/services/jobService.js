import api from "./api";

// Get all jobs for the current user
export const getJobs = async () => {
  const response = await api.get("/jobs/", {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  });
  return response.data;
};

// Get open jobs (public endpoint)
export const getOpenJobs = async () => {
  const response = await api.get("/jobs/open");
  return response.data;
};

// Search jobs by title, company, or location
export const searchJobs = async (params) => {
  const response = await api.get("/jobs/search", {
    params: params,
  });
  return response.data;
};

// Get job recommendations for a resume
export const getJobRecommendations = async (resumePublicId, topN = 10, minMatch = null) => {
  const params = {
    top_n: topN,
  };
  if (minMatch !== null) {
    params.min_match = minMatch;
  }
  
  const response = await api.get(`/matches/recommendations/${resumePublicId}`, {
    params: params,
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  });
  return response.data;
};

// Get matches for a specific resume
export const getResumeMatches = async (resumePublicId) => {
  const response = await api.get(`/matches/resume/${resumePublicId}`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  });
  return response.data;
};

// Get specific match between resume and job
export const getMatch = async (resumePublicId, jobPublicId) => {
  const response = await api.get(`/matches/${resumePublicId}/${jobPublicId}`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  });
  return response.data;
};

// Generate a comprehensive match between resume and job
export const generateMatch = async (resumePublicId, jobPublicId) => {
  const response = await api.post(`/matches/generate/${resumePublicId}/${jobPublicId}`, {}, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  });
  return response.data;
};

// Create a new job
export const createJob = async (jobData) => {
  const response = await api.post("/jobs/", jobData, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  });
  return response.data;
};

// Get specific job details
export const getJob = async (jobPublicId) => {
  const response = await api.get(`/jobs/${jobPublicId}`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  });
  return response.data;
};
