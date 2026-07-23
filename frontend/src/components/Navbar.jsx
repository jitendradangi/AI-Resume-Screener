import { FaBell, FaSignOutAlt, FaUserCircle, FaSun, FaMoon, FaBars } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useTheme } from "../context/ThemeContext";
import { useSidebar } from "../context/SidebarContext";

function Navbar() {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const { theme, toggleTheme } = useTheme();
  const { isOpen, toggleSidebar } = useSidebar();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <header className="sticky top-0 z-30 flex h-16 w-full items-center justify-between border-b border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 px-6 backdrop-blur-md">
      <div className="flex items-center gap-4">
        {!isOpen && (
          <button 
            onClick={toggleSidebar} 
            className="rounded-full p-2 text-slate-500 dark:text-slate-400 transition-colors hover:bg-slate-100 dark:hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <FaBars className="h-5 w-5" />
          </button>
        )}
        <h2 className="text-xl font-semibold text-slate-800 dark:text-white lg:hidden">Dashboard</h2>
      </div>
      <div className="hidden lg:block"></div>
      
      <div className="flex items-center gap-4 sm:gap-6">
        <button 
          onClick={toggleTheme}
          className="rounded-full p-2 text-slate-500 dark:text-slate-400 transition-colors hover:bg-slate-100 dark:hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        >
          {theme === "light" ? <FaMoon className="h-5 w-5" /> : <FaSun className="h-5 w-5" />}
        </button>

        <button className="rounded-full p-2 text-slate-500 dark:text-slate-400 transition-colors hover:bg-slate-100 dark:hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500">
          <FaBell className="h-5 w-5" />
        </button>
        
        <div className="flex items-center gap-2 border-l border-slate-200 dark:border-slate-700 pl-4 sm:pl-6">
          <FaUserCircle className="h-8 w-8 text-slate-400 dark:text-slate-500" />
          <span className="hidden text-sm font-medium text-slate-700 dark:text-slate-200 sm:block">Jitendra</span>
        </div>
        
        <button
          className="flex items-center gap-2 rounded-lg bg-white dark:bg-slate-800 px-3 py-2 text-sm font-medium text-rose-600 dark:text-rose-400 transition-colors hover:bg-rose-50 dark:hover:bg-rose-900/30 border border-rose-200 dark:border-rose-900/50 focus:outline-none focus:ring-2 focus:ring-rose-500"
          onClick={handleLogout}
        >
          <FaSignOutAlt className="h-4 w-4" />
          <span className="hidden sm:inline">Logout</span>
        </button>
      </div>
    </header>
  );
}

export default Navbar;