import { NavLink } from "react-router-dom";
import {
  FaHome,
  FaFileUpload,
  FaFileAlt,
  FaBullseye,
  FaBriefcase,
  FaUser,
  FaTimes,
} from "react-icons/fa";
import { useSidebar } from "../context/SidebarContext";

function Sidebar() {
  const { isOpen, toggleSidebar } = useSidebar();

  const linkClass = ({ isActive }) =>
    `flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium transition-all ${
      isActive
        ? "bg-indigo-50 dark:bg-indigo-900/40 text-indigo-700 dark:text-indigo-400"
        : "text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-slate-900 dark:hover:text-slate-200"
    }`;

  if (!isOpen) return null;

  return (
    <aside className="w-64 flex-col border-r border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 flex shadow-sm shrink-0 h-full">
      <div className="flex h-16 items-center justify-between border-b border-slate-200 dark:border-slate-800 px-6">
        <h2 className="text-2xl font-extrabold bg-gradient-to-r from-indigo-600 to-violet-600 dark:from-indigo-400 dark:to-violet-400 bg-clip-text text-transparent">AI Resume</h2>
        <button 
          onClick={toggleSidebar} 
          className="rounded-full p-2 text-slate-500 dark:text-slate-400 transition-colors hover:bg-slate-100 dark:hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        >
          <FaTimes className="h-5 w-5" />
        </button>
      </div>

      <nav className="flex-1 space-y-1.5 overflow-y-auto p-4">
        <NavLink to="/dashboard" className={linkClass}>
          <FaHome className="h-5 w-5" /> Home
        </NavLink>

        <NavLink to="/upload" className={linkClass}>
          <FaFileUpload className="h-5 w-5" /> Upload Resume
        </NavLink>

        <NavLink to="/my-resumes" className={linkClass}>
          <FaFileAlt className="h-5 w-5" /> My Resumes
        </NavLink>

        <NavLink to="/ats-score" className={linkClass}>
          <FaBullseye className="h-5 w-5" /> ATS Score
        </NavLink>

        <NavLink to="/jobs" className={linkClass}>
          <FaBriefcase className="h-5 w-5" /> Jobs
        </NavLink>

        <NavLink to="/profile" className={linkClass}>
          <FaUser className="h-5 w-5" /> Profile
        </NavLink>
      </nav>
    </aside>
  );
}

export default Sidebar;