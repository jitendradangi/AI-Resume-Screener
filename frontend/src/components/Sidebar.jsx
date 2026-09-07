import { NavLink } from "react-router-dom";
import {
  FaHome,
  FaFileUpload,
  FaFileAlt,
  FaBullseye,
  FaBriefcase,
  FaUser,
  FaTimes,
  FaMagic,
} from "react-icons/fa";
import { useSidebar } from "../context/SidebarContext";

function Sidebar() {
  const { isOpen, toggleSidebar } = useSidebar();

  const linkClass = ({ isActive }) =>
    `flex items-center gap-3 rounded-xl px-3.5 py-2.5 text-xs font-semibold transition-all duration-200 ${
      isActive
        ? "bg-gradient-to-r from-indigo-500/15 via-indigo-500/10 to-purple-500/10 border border-indigo-500/30 text-indigo-300 shadow-[0_0_15px_rgba(99,102,241,0.1)]"
        : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60 border border-transparent"
    }`;

  if (!isOpen) return null;

  return (
    <>
      {/* Mobile Drawer Overlay Backdrop */}
      <div 
        onClick={toggleSidebar}
        className="fixed inset-0 bg-slate-950/70 backdrop-blur-sm z-40 lg:hidden"
      ></div>

      <aside className="fixed lg:static inset-y-0 left-0 z-50 w-64 flex-col border-r border-slate-800/80 bg-slate-900/95 backdrop-blur-2xl flex shadow-2xl shrink-0 h-full">
        {/* Header Branding */}
        <div className="flex h-16 items-center justify-between border-b border-slate-800/80 px-5">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-indigo-600 via-indigo-500 to-purple-500 p-0.5 shadow-md flex items-center justify-center">
              <div className="w-full h-full bg-slate-950 rounded-[6px] flex items-center justify-center">
                <FaFileAlt className="text-indigo-400 text-xs" />
              </div>
            </div>
            <span className="text-base font-bold tracking-tight text-white">
              AI Resume <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-purple-400">Screener</span>
            </span>
          </div>
          <button 
            onClick={toggleSidebar} 
            aria-label="Close Sidebar"
            className="rounded-lg p-1.5 text-slate-400 hover:text-white transition-colors hover:bg-slate-800 border border-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500/40"
          >
            <FaTimes className="h-4 w-4" />
          </button>
        </div>

        {/* Nav Links */}
        <nav className="flex-1 space-y-6 overflow-y-auto p-4">
          
          {/* Section 1: Workflow */}
          <div>
            <p className="text-[10px] font-bold text-slate-500 tracking-wider uppercase mb-2 px-3">
              Core Workflow
            </p>
            <div className="space-y-1">
              <NavLink to="/dashboard" className={linkClass}>
                <FaHome className="h-4 w-4 flex-shrink-0 text-indigo-400" /> 
                <span>Home</span>
              </NavLink>

              <NavLink to="/upload" className={linkClass}>
                <FaFileUpload className="h-4 w-4 flex-shrink-0 text-indigo-400" /> 
                <span>Upload Resume</span>
              </NavLink>

              <NavLink to="/my-resumes" className={linkClass}>
                <FaFileAlt className="h-4 w-4 flex-shrink-0 text-indigo-400" /> 
                <span>My Resumes</span>
              </NavLink>

              <NavLink to="/ats-score" className={linkClass}>
                <FaBullseye className="h-4 w-4 flex-shrink-0 text-indigo-400" /> 
                <span>ATS Score</span>
              </NavLink>
            </div>
          </div>

          <div className="border-t border-slate-800/80 my-2"></div>

          {/* Section 2: Account & Discovery */}
          <div>
            <p className="text-[10px] font-bold text-slate-500 tracking-wider uppercase mb-2 px-3">
              Discovery & Account
            </p>
            <div className="space-y-1">
              <NavLink to="/jobs" className={linkClass}>
                <FaBriefcase className="h-4 w-4 flex-shrink-0 text-indigo-400" /> 
                <span>Jobs</span>
              </NavLink>

              <NavLink to="/profile" className={linkClass}>
                <FaUser className="h-4 w-4 flex-shrink-0 text-indigo-400" /> 
                <span>Profile</span>
              </NavLink>
            </div>
          </div>

        </nav>

        {/* Footer Pro Badge Callout */}
        <div className="p-4 border-t border-slate-800/80">
          <div className="rounded-xl bg-gradient-to-r from-indigo-950/60 to-purple-950/60 border border-indigo-500/20 p-3 flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center border border-indigo-500/30 flex-shrink-0">
              <FaMagic className="text-xs" />
            </div>
            <div>
              <p className="text-xs font-semibold text-white">AI Engine Active</p>
              <p className="text-[10px] text-slate-400">GPT-4 Analysis Ready</p>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
}

export default Sidebar;