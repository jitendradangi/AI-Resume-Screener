import { FaBell, FaSignOutAlt, FaSun, FaMoon, FaBars } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useTheme } from "../context/ThemeContext";
import { useSidebar } from "../context/SidebarContext";

function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme();
  const { isOpen, toggleSidebar } = useSidebar();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  const userInitial = user?.full_name 
    ? user.full_name.charAt(0).toUpperCase() 
    : (user?.email ? user.email.charAt(0).toUpperCase() : "U");

  const displayName = user?.full_name || (user?.email ? user.email.split("@")[0] : "User");

  return (
    <header className="sticky top-0 z-30 flex h-16 w-full items-center justify-between border-b border-slate-800/80 bg-slate-950/80 px-4 sm:px-6 backdrop-blur-xl shadow-md">
      <div className="flex items-center gap-3">
        {!isOpen && (
          <button 
            onClick={toggleSidebar} 
            aria-label="Open Sidebar"
            className="rounded-xl p-2 text-slate-400 hover:text-white transition-colors bg-slate-900 hover:bg-slate-800 border border-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500/40"
          >
            <FaBars className="h-4 w-4" />
          </button>
        )}
        <h2 className="text-lg font-bold tracking-tight text-white lg:hidden">
          AI Resume <span className="text-indigo-400">Screener</span>
        </h2>
      </div>
      
      <div className="hidden lg:block"></div>
      
      <div className="flex items-center gap-3 sm:gap-4">
        {/* Theme Toggle Button */}
        <button 
          onClick={toggleTheme}
          aria-label="Toggle Theme"
          className="w-9 h-9 rounded-xl flex items-center justify-center bg-slate-900 border border-slate-800 text-slate-400 hover:text-white hover:border-slate-700 transition-all shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/40"
        >
          {theme === "light" ? <FaMoon className="h-4 w-4 text-indigo-400" /> : <FaSun className="h-4 w-4 text-amber-400" />}
        </button>

        {/* Notifications Button */}
        <button 
          aria-label="Notifications"
          className="relative w-9 h-9 rounded-xl flex items-center justify-center bg-slate-900 border border-slate-800 text-slate-400 hover:text-white hover:border-slate-700 transition-all shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/40"
        >
          <FaBell className="h-4 w-4" />
          <span className="absolute top-2 right-2 w-2 h-2 rounded-full bg-indigo-500 animate-pulse"></span>
        </button>
        
        {/* User Profile Pill */}
        <div className="flex items-center gap-2.5 border-l border-slate-800 pl-3 sm:pl-4">
          <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-indigo-500 via-indigo-600 to-purple-600 text-white font-bold text-xs flex items-center justify-center border border-white/10 shadow-sm flex-shrink-0">
            {userInitial}
          </div>
          <span className="hidden text-xs font-semibold text-slate-200 sm:block">
            {displayName}
          </span>
        </div>
        
        {/* Refined Logout Button */}
        <button
          className="flex items-center gap-2 rounded-xl bg-slate-900 border border-slate-800 hover:border-rose-500/40 px-3 py-2 text-xs font-semibold text-slate-300 hover:text-rose-400 hover:bg-rose-500/10 transition-all shadow-sm focus:outline-none focus:ring-2 focus:ring-rose-500/40"
          onClick={handleLogout}
        >
          <FaSignOutAlt className="h-3.5 w-3.5 text-slate-400 group-hover:text-rose-400" />
          <span className="hidden sm:inline">Logout</span>
        </button>
      </div>
    </header>
  );
}

export default Navbar;

