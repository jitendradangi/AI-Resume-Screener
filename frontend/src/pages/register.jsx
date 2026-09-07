import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { registerUser } from "../services/authService";
import { 
  FaUser, 
  FaEnvelope, 
  FaLock, 
  FaEye, 
  FaEyeSlash, 
  FaCheckCircle, 
  FaFileAlt, 
  FaBrain, 
  FaBriefcase, 
  FaChartLine, 
  FaArrowRight, 
  FaGoogle, 
  FaGithub,
  FaMagic
} from "react-icons/fa";

function Register() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    full_name: "",
    email: "",
    password: "",
  });

  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState("error");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");

    try {
      await registerUser(formData);
      setMessage("Registration successful! Redirecting to login...");
      setMessageType("success");

      setTimeout(() => {
        navigate("/");
      }, 2000);
    } catch (error) {
      if (error.response) {
        setMessage(error.response.data.detail || "Registration failed");
        setMessageType("error");
      } else {
        setMessage("Server Error");
        setMessageType("error");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col justify-center relative overflow-hidden font-sans selection:bg-indigo-500/30 selection:text-indigo-200">
      {/* Background Decorative Mesh & Glow Blobs */}
      <div className="absolute inset-0 bg-grid-pattern opacity-40 pointer-events-none"></div>
      <div className="absolute -top-40 -left-40 w-96 h-96 bg-indigo-600/20 rounded-full blur-[128px] pointer-events-none animate-pulse-slow"></div>
      <div className="absolute -bottom-40 -right-40 w-96 h-96 bg-purple-600/20 rounded-full blur-[128px] pointer-events-none animate-pulse-slow"></div>
      <div className="absolute top-1/2 left-1/3 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-violet-600/10 rounded-full blur-[140px] pointer-events-none"></div>
      <div className="absolute inset-0 bg-radial-gradient pointer-events-none"></div>

      <div className="min-h-screen grid grid-cols-1 lg:grid-cols-12 relative z-10 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-6 sm:py-8 lg:py-0 items-center gap-6 sm:gap-8 lg:gap-12">
        
        {/* Left Panel - Marketing & Live Diagnostics Preview */}
        <div className="lg:col-span-7 flex flex-col justify-center py-2 sm:py-4 lg:py-8">
          
          {/* Brand Logo */}
          <div className="flex items-center gap-3 mb-4 sm:mb-6">
            <div className="w-9 sm:w-10 h-9 sm:h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-purple-500 p-0.5 shadow-lg shadow-indigo-500/20 flex items-center justify-center">
              <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
                <FaFileAlt className="text-indigo-400 text-base sm:text-lg" />
              </div>
            </div>
            <span className="text-lg sm:text-xl font-bold tracking-tight text-white">
              AI Resume <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-purple-400">Screener</span>
            </span>
          </div>

          {/* Social Proof Pill */}
          <div className="inline-flex items-center gap-2 px-3 sm:px-3.5 py-1 sm:py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/20 backdrop-blur-md text-[11px] sm:text-xs font-medium text-indigo-300 w-fit mb-4 sm:mb-6 shadow-sm">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span>AI-Powered • Trusted by 10,000+ Job Seekers</span>
          </div>
          
          {/* Main Headline */}
          <h1 className="text-2xl sm:text-4xl lg:text-5xl font-extrabold text-white tracking-tight leading-[1.15] mb-3 sm:mb-4">
            Build a stronger resume. <br className="hidden sm:inline" />
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 via-purple-300 to-pink-400">
              Get hired 3x faster.
            </span>
          </h1>
          <p className="text-slate-400 text-sm sm:text-base lg:text-lg mb-6 sm:mb-8 max-w-xl leading-relaxed">
            Join thousands of professionals optimizing their resumes with instant AI feedback and intelligent keyword scoring.
          </p>

          {/* Product Preview Card */}
          <div className="relative rounded-2xl bg-slate-900/80 backdrop-blur-xl border border-slate-800/90 shadow-[0_20px_50px_rgba(0,0,0,0.5)] overflow-hidden group hover:border-indigo-500/30 transition-all duration-300 mb-6 sm:mb-8">
            <div className="absolute -right-20 -bottom-20 w-64 h-64 bg-indigo-500/10 rounded-full blur-3xl group-hover:bg-indigo-500/15 transition-all duration-500"></div>
            
            {/* Card Header */}
            <div className="flex flex-wrap sm:flex-nowrap items-center justify-between gap-3 p-4 sm:p-6 pb-4 border-b border-slate-800/80">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center border border-indigo-500/30 flex-shrink-0">
                  <FaMagic className="text-xs" />
                </div>
                <div>
                  <h3 className="text-white font-semibold text-xs sm:text-sm">Resume Analysis Diagnostics</h3>
                  <p className="text-slate-400 text-[11px] sm:text-xs">Senior Full Stack Engineer Role</p>
                </div>
              </div>
              <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-[11px] font-medium flex-shrink-0">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                <span>Live Demo</span>
              </div>
            </div>
            
            {/* Main Score Showcase */}
            <div className="p-4 sm:p-6 grid grid-cols-1 sm:grid-cols-12 gap-5 sm:gap-6 items-center">
              
              {/* Circular ATS Ring */}
              <div className="sm:col-span-5 flex items-center gap-4 bg-slate-950/60 p-3.5 sm:p-4 rounded-xl border border-slate-800/80 h-full">
                <div className="relative w-16 h-16 flex-shrink-0">
                  <svg className="w-16 h-16 transform -rotate-90" viewBox="0 0 80 80">
                    <defs>
                      <linearGradient id="atsGradientReg" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="#818CF8" />
                        <stop offset="100%" stopColor="#C084FC" />
                      </linearGradient>
                    </defs>
                    <circle cx="40" cy="40" r="32" stroke="#1E293B" strokeWidth="6" fill="none" />
                    <circle 
                      cx="40" 
                      cy="40" 
                      r="32" 
                      stroke="url(#atsGradientReg)" 
                      strokeWidth="6" 
                      fill="none" 
                      strokeDasharray="201.06" 
                      strokeDashoffset="26.1" 
                      strokeLinecap="round" 
                      className="transition-all duration-1000 ease-out"
                    />
                  </svg>
                  <div className="absolute inset-0 flex items-center justify-center flex-col">
                    <span className="text-white font-extrabold text-lg leading-none">87</span>
                    <span className="text-[9px] text-indigo-300 font-medium mt-0.5">/100</span>
                  </div>
                </div>
                <div>
                  <p className="text-white font-semibold text-xs sm:text-sm">ATS Score</p>
                  <span className="inline-block mt-1 px-2 py-0.5 rounded-md bg-emerald-500/10 text-emerald-400 text-[11px] font-medium border border-emerald-500/20">
                    Top 5% Match
                  </span>
                </div>
              </div>

              {/* Quick Metrics Progress Fills */}
              <div className="sm:col-span-7 space-y-3 flex flex-col justify-center">
                <div>
                  <div className="flex items-center justify-between text-xs mb-1">
                    <span className="text-slate-300 font-medium truncate pr-2">Skills Relevance</span>
                    <span className="w-10 text-right font-semibold text-indigo-300 flex-shrink-0">92%</span>
                  </div>
                  <div className="w-full bg-slate-950 rounded-full h-2 p-0.5 border border-slate-800 overflow-hidden">
                    <div className="bg-gradient-to-r from-indigo-500 to-purple-500 h-1.5 rounded-full transition-all duration-1000" style={{ width: '92%' }}></div>
                  </div>
                </div>

                <div>
                  <div className="flex items-center justify-between text-xs mb-1">
                    <span className="text-slate-300 font-medium truncate pr-2">Experience Fit</span>
                    <span className="w-10 text-right font-semibold text-purple-300 flex-shrink-0">84%</span>
                  </div>
                  <div className="w-full bg-slate-950 rounded-full h-2 p-0.5 border border-slate-800 overflow-hidden">
                    <div className="bg-gradient-to-r from-purple-500 to-pink-500 h-1.5 rounded-full transition-all duration-1000" style={{ width: '84%' }}></div>
                  </div>
                </div>

                <div>
                  <div className="flex items-center justify-between text-xs mb-1">
                    <span className="text-slate-300 font-medium truncate pr-2">Keyword Density</span>
                    <span className="w-10 text-right font-semibold text-cyan-300 flex-shrink-0">91%</span>
                  </div>
                  <div className="w-full bg-slate-950 rounded-full h-2 p-0.5 border border-slate-800 overflow-hidden">
                    <div className="bg-gradient-to-r from-cyan-500 to-indigo-500 h-1.5 rounded-full transition-all duration-1000" style={{ width: '91%' }}></div>
                  </div>
                </div>
              </div>

            </div>

            {/* Bottom Summary Footer Strip */}
            <div className="bg-indigo-950/50 border-t border-indigo-500/20 px-4 sm:px-5 py-3 flex flex-wrap sm:flex-nowrap items-center justify-between text-xs text-indigo-200 gap-2">
              <span className="flex items-center gap-2 text-xs">
                <FaCheckCircle className="text-emerald-400 text-xs flex-shrink-0" />
                <span>14 core skills matched • 3 high-impact keywords suggested</span>
              </span>
              <span className="font-semibold text-indigo-300 hover:text-white transition-colors cursor-pointer text-[11px] whitespace-nowrap">
                View Breakdown &rarr;
              </span>
            </div>
          </div>

          {/* Feature Badges Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div className="bg-slate-900/60 backdrop-blur-md border border-slate-800/80 rounded-xl p-3 flex items-center gap-3 hover:border-indigo-500/30 hover:bg-slate-900/80 transition-all">
              <div className="w-9 h-9 rounded-lg bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 flex items-center justify-center flex-shrink-0">
                <FaBrain className="text-sm" />
              </div>
              <div>
                <h4 className="text-white text-xs font-semibold">AI Analysis</h4>
                <p className="text-slate-400 text-[11px]">Instant deep scoring</p>
              </div>
            </div>

            <div className="bg-slate-900/60 backdrop-blur-md border border-slate-800/80 rounded-xl p-3 flex items-center gap-3 hover:border-purple-500/30 hover:bg-slate-900/80 transition-all">
              <div className="w-9 h-9 rounded-lg bg-purple-500/10 border border-purple-500/20 text-purple-400 flex items-center justify-center flex-shrink-0">
                <FaChartLine className="text-sm" />
              </div>
              <div>
                <h4 className="text-white text-xs font-semibold">ATS Scanner</h4>
                <p className="text-slate-400 text-[11px]">Bypass recruiter filters</p>
              </div>
            </div>

            <div className="bg-slate-900/60 backdrop-blur-md border border-slate-800/80 rounded-xl p-3 flex items-center gap-3 hover:border-cyan-500/30 hover:bg-slate-900/80 transition-all">
              <div className="w-9 h-9 rounded-lg bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 flex items-center justify-center flex-shrink-0">
                <FaBriefcase className="text-sm" />
              </div>
              <div>
                <h4 className="text-white text-xs font-semibold">Smart Match</h4>
                <p className="text-slate-400 text-[11px]">Tailor per job posting</p>
              </div>
            </div>
          </div>

        </div>

        {/* Right Panel - Register Form */}
        <div className="lg:col-span-5 flex flex-col justify-center py-2 sm:py-4 lg:py-8">
          
          <div className="w-full max-w-md mx-auto bg-slate-900/90 backdrop-blur-2xl border border-slate-800/90 rounded-2xl p-5 sm:p-8 shadow-[0_25px_60px_-15px_rgba(0,0,0,0.7)] relative overflow-hidden">
            {/* Top Border Highlight Glow */}
            <div className="absolute top-0 left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-indigo-500 to-transparent opacity-60"></div>
            
            {/* Card Header */}
            <div className="mb-5 sm:mb-6">
              <h2 className="text-xl sm:text-2xl lg:text-3xl font-extrabold text-white tracking-tight">Create an account</h2>
              <p className="text-slate-400 text-xs sm:text-sm mt-1">Start optimizing your resume with AI in minutes</p>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit} className="space-y-3.5 sm:space-y-4">
              <div>
                <label className="block text-[11px] sm:text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                  Full Name
                </label>
                <div className="relative flex items-center">
                  <div className="absolute left-3.5 text-slate-400 text-xs sm:text-sm pointer-events-none">
                    <FaUser />
                  </div>
                  <input
                    type="text"
                    name="full_name"
                    placeholder="John Doe"
                    value={formData.full_name}
                    onChange={handleChange}
                    className="w-full pl-9 sm:pl-10 pr-4 py-2.5 sm:py-3 rounded-xl bg-slate-950/70 border border-slate-800 text-white text-xs sm:text-sm placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/30 focus:border-indigo-500 transition-all duration-200"
                    required
                  />
                </div>
              </div>

              <div>
                <label className="block text-[11px] sm:text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                  Email Address
                </label>
                <div className="relative flex items-center">
                  <div className="absolute left-3.5 text-slate-400 text-xs sm:text-sm pointer-events-none">
                    <FaEnvelope />
                  </div>
                  <input
                    type="email"
                    name="email"
                    placeholder="you@example.com"
                    value={formData.email}
                    onChange={handleChange}
                    className="w-full pl-9 sm:pl-10 pr-4 py-2.5 sm:py-3 rounded-xl bg-slate-950/70 border border-slate-800 text-white text-xs sm:text-sm placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/30 focus:border-indigo-500 transition-all duration-200"
                    required
                  />
                </div>
              </div>

              <div>
                <label className="block text-[11px] sm:text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                  Password
                </label>
                <div className="relative flex items-center">
                  <div className="absolute left-3.5 text-slate-400 text-xs sm:text-sm pointer-events-none">
                    <FaLock />
                  </div>
                  <input
                    type={showPassword ? "text" : "password"}
                    name="password"
                    placeholder="••••••••"
                    value={formData.password}
                    onChange={handleChange}
                    className="w-full pl-9 sm:pl-10 pr-10 sm:pr-11 py-2.5 sm:py-3 rounded-xl bg-slate-950/70 border border-slate-800 text-white text-xs sm:text-sm placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/30 focus:border-indigo-500 transition-all duration-200"
                    required
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    aria-label={showPassword ? "Hide password" : "Show password"}
                    className="absolute right-3.5 text-slate-400 hover:text-slate-200 text-xs sm:text-sm transition-colors focus:outline-none"
                  >
                    {showPassword ? <FaEyeSlash /> : <FaEye />}
                  </button>
                </div>
              </div>

              <div className="flex items-center pt-0.5">
                <input
                  type="checkbox"
                  id="terms"
                  className="w-4 h-4 text-indigo-600 bg-slate-950 border-slate-800 rounded focus:ring-indigo-500/40 focus:ring-2 accent-indigo-600"
                  required
                />
                <label htmlFor="terms" className="ml-2.5 text-xs text-slate-400">
                  I agree to the <Link to="#" className="text-indigo-400 hover:underline">Terms of Service</Link> and <Link to="#" className="text-indigo-400 hover:underline">Privacy Policy</Link>
                </label>
              </div>

              <button 
                type="submit"
                disabled={loading}
                className="w-full py-3 sm:py-3.5 px-4 bg-gradient-to-r from-indigo-600 via-indigo-500 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-semibold text-xs sm:text-sm rounded-xl shadow-lg shadow-indigo-600/25 hover:shadow-indigo-500/40 hover:scale-[1.01] active:scale-[0.99] focus:outline-none focus:ring-2 focus:ring-indigo-500/50 transition-all duration-200 disabled:opacity-60 disabled:cursor-not-allowed disabled:hover:scale-100 flex items-center justify-center gap-2 mt-1"
              >
                {loading ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                    <span>Creating account...</span>
                  </>
                ) : (
                  <>
                    <span>Create account</span>
                    <FaArrowRight className="text-xs" />
                  </>
                )}
              </button>
            </form>

            {message && (
              <div className={`mt-3 sm:mt-4 p-2.5 sm:p-3.5 rounded-xl text-xs text-center flex items-center justify-center leading-normal border ${
                messageType === 'success' 
                  ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-300' 
                  : 'bg-rose-500/10 border-rose-500/20 text-rose-300'
              }`}>
                {message}
              </div>
            )}

            {/* Social Divider & Row */}
            <div className="relative my-4 sm:my-6 text-center text-xs">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-slate-800"></div>
              </div>
              <span className="relative px-3 bg-slate-900 text-slate-400 font-medium text-[11px] sm:text-xs">
                or continue with
              </span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 sm:gap-3">
              <button 
                type="button"
                className="flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl bg-slate-950/60 border border-slate-800 hover:border-slate-700 text-slate-300 text-xs font-medium hover:bg-slate-800/50 hover:text-white transition-all cursor-pointer"
              >
                <FaGoogle className="text-rose-400 text-sm" />
                <span>Google</span>
              </button>
              <button 
                type="button"
                className="flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl bg-slate-950/60 border border-slate-800 hover:border-slate-700 text-slate-300 text-xs font-medium hover:bg-slate-800/50 hover:text-white transition-all cursor-pointer"
              >
                <FaGithub className="text-slate-200 text-sm" />
                <span>GitHub</span>
              </button>
            </div>

            {/* Sign in link */}
            <div className="mt-4 sm:mt-6 text-center text-xs text-slate-400">
              Already have an account?{" "}
              <Link to="/" className="font-semibold text-indigo-400 hover:text-indigo-300 hover:underline transition-colors">
                Sign in
              </Link>
            </div>

            {/* Footer Terms Note */}
            <p className="mt-4 sm:mt-6 text-center text-[10px] sm:text-[11px] text-slate-500 leading-normal sm:leading-relaxed max-w-xs sm:max-w-none mx-auto">
              Protected by enterprise-grade encryption. By continuing, you agree to our Terms of Service and Privacy Policy.
            </p>

          </div>

        </div>

      </div>
    </div>
  );
}

export default Register;


