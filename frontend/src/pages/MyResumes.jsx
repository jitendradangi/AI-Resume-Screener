import { useEffect, useState } from "react";
import DashboardLayout from "../layouts/DashboardLayout";
import {getMyResumes,deleteResume} from "../services/resumeService";
import { FaFilePdf, FaFileWord } from "react-icons/fa";

const getFileIcon = (filename) => {
  const extension = filename.split(".").pop().toLowerCase();

  switch (extension) {
    case "pdf":
      return <FaFilePdf color="#e53935" size={22} />;

    case "doc":
    case "docx":
      return <FaFileWord color="#1565c0" size={22} />;

    default:
      return null;
  }
};

const formatFilename = (filename) => {
  if (!filename) return "";
  const parts = filename.split('_');
  // UUID length is 36 characters (e.g., 51ec59e4-9438-4887-b465-3a4f47747968)
  if (parts.length > 1 && parts[0].length === 36) {
    return parts.slice(1).join('_');
  }
  return filename;
};

function MyResumes() {
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchResumes = async () => {
    try {
      const data = await getMyResumes();
      setResumes(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchResumes();
  }, []);

  const handleDelete = async (id) => {
    const confirmDelete = window.confirm(
      "Delete this resume?"
    );

    if (!confirmDelete) return;

    try {
      await deleteResume(id);

      setResumes((prev) =>
        prev.filter((resume) => resume.id !== id)
      );
    } catch (err) {
      alert("Delete failed.");
    }
  };

  if (loading) return <h3>Loading...</h3>;

  return (
    <DashboardLayout>
      <div className="max-w-6xl mx-auto py-8">
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-slate-900 dark:text-white">My Resumes</h2>
            <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">Manage your uploaded resumes</p>
          </div>
        </div>

        {resumes.length === 0 ? (
          <div className="flex flex-col items-center justify-center p-12 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl border-dashed">
            <p className="text-slate-500 dark:text-slate-400 mb-4">No resumes uploaded yet.</p>
            <a href="/upload" className="text-sm font-medium text-indigo-600 dark:text-indigo-400 hover:text-indigo-700 dark:hover:text-indigo-300">Upload your first resume</a>
          </div>
        ) : (
          <div className="overflow-hidden rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-sm">
            <table className="min-w-full divide-y divide-slate-200 dark:divide-slate-800 text-left text-sm">
              <thead className="bg-slate-50 dark:bg-slate-800/50">
                <tr>
                  <th scope="col" className="px-6 py-4 font-medium text-slate-900 dark:text-white">Filename</th>
                  <th scope="col" className="px-6 py-4 font-medium text-slate-900 dark:text-white">Uploaded</th>
                  <th scope="col" className="px-6 py-4 font-medium text-slate-900 dark:text-white text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200 dark:divide-slate-800 bg-white dark:bg-slate-900">
                {resumes.map((resume) => (
                  <tr key={resume.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center gap-3">
                        {getFileIcon(resume.filename)}
                        <span className="font-medium text-slate-900 dark:text-slate-200">{formatFilename(resume.filename)}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-slate-500 dark:text-slate-400">
                      {new Date(resume.uploaded_at).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right">
                      <button
                        onClick={() => handleDelete(resume.id)}
                        className="text-rose-600 dark:text-rose-400 hover:text-rose-700 dark:hover:text-rose-300 hover:bg-rose-50 dark:hover:bg-rose-900/30 px-3 py-1.5 rounded-lg transition-colors font-medium focus:outline-none focus:ring-2 focus:ring-rose-500/20"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}

export default MyResumes;