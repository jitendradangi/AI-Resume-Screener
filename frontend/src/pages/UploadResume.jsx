import { useState } from "react";
import DashboardLayout from "../layouts/DashboardLayout";
import { uploadResume } from "../services/resumeService";
import { ALLOWED_FILE_TYPES, MAX_FILE_SIZE,} from "../constants/fileConstants";

function UploadResume() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  
  const validateFile = (selectedFile) => {
  if (!selectedFile) return false;

  if (!ALLOWED_FILE_TYPES.includes(selectedFile.type)) {
    setMessage("❌ Only PDF and Word documents are allowed.");
    return false;
  }

  if (selectedFile.size > MAX_FILE_SIZE) {
    setMessage("❌ File size must be less than 5 MB.");
    return false;
  }

  return true;
};

  const handleFileChange = (e) => {
  const selectedFile = e.target.files[0];

  if (!validateFile(selectedFile)) {
    setFile(null);
    return;
  }

  setFile(selectedFile);
  setMessage("");
};

  const handleDrop = (e) => {
  e.preventDefault();

  const selectedFile = e.dataTransfer.files[0];

  if (!validateFile(selectedFile)) {
    setFile(null);
    return;
  }

  setFile(selectedFile);
  setMessage("");
};

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      setMessage("Please select a resume.");
      return;
    }

    try {
      setLoading(true);
      setMessage("");

      await uploadResume(file);

      setMessage("✅ Resume uploaded successfully!");
      setFile(null);

      // Clear the file input
      e.target.reset();
    } catch (error) {
      setMessage("❌ Upload failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <DashboardLayout>
      <div className="max-w-3xl mx-auto py-8">
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white">Upload Resume</h2>
          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">Upload your resume to get an AI-powered ATS score</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <label
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            className="flex flex-col items-center justify-center w-full h-64 border-2 border-slate-300 dark:border-slate-700 border-dashed rounded-2xl cursor-pointer bg-slate-50 dark:bg-slate-900/50 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
          >
            <div className="flex flex-col items-center justify-center pt-5 pb-6">
              <svg className="w-10 h-10 mb-4 text-slate-400 dark:text-slate-500" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 16">
                  <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"/>
              </svg>
              <h3 className="mb-2 text-sm font-semibold text-slate-700 dark:text-slate-300">Drag & Drop Resume</h3>
              <p className="text-xs text-slate-500 dark:text-slate-400">or Click to Browse (PDF, DOC, DOCX up to 5MB)</p>
            </div>
            <input
              type="file"
              accept=".pdf,.doc,.docx"
              className="hidden"
              onChange={handleFileChange}
            />
          </label>

          {file && (
            <div className="flex items-center p-4 bg-indigo-50 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-400 rounded-lg border border-indigo-100 dark:border-indigo-900/50">
              <svg className="w-5 h-5 mr-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                <path d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" />
              </svg>
              <span className="font-medium truncate">{file.name}</span>
            </div>
          )}

          <button 
            type="submit" 
            disabled={loading || !file}
            className="w-full sm:w-auto px-6 py-3 bg-indigo-600 text-white font-medium rounded-lg shadow-sm hover:bg-indigo-700 focus:ring-4 focus:ring-indigo-300 transition-all disabled:opacity-60 disabled:cursor-not-allowed"
          > 
            {loading ? "Uploading..." : "Upload Resume"} 
          </button>
        </form>

        {message && (
          <div className={`mt-6 p-4 rounded-lg text-sm font-medium border ${message.includes('✅') ? 'bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400 border-emerald-200 dark:border-emerald-900/50' : 'bg-rose-50 dark:bg-rose-900/30 text-rose-700 dark:text-rose-400 border-rose-200 dark:border-rose-900/50'}`}>
            {message}
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}

export default UploadResume;