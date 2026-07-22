import { NavLink } from "react-router-dom";
import {
  FaHome,
  FaFileUpload,
  FaFileAlt,
  FaBullseye,
  FaBriefcase,
  FaUser,
} from "react-icons/fa";

function Sidebar() {
  return (
    <div className="sidebar">
      <h2 className="logo">AI Resume</h2>

      <nav>
        <NavLink to="/dashboard" className="nav-link">
          <FaHome /> Home
        </NavLink>

        <NavLink to="/upload" className="nav-link">
          <FaFileUpload /> Upload Resume
        </NavLink>

        <NavLink to="/my-resumes" className="nav-link">
          <FaFileAlt /> My Resumes
        </NavLink>

        <NavLink to="/ats-score" className="nav-link">
          <FaBullseye /> ATS Score
        </NavLink>

        <NavLink to="/jobs" className="nav-link">
          <FaBriefcase /> Jobs
        </NavLink>

        <NavLink to="/profile" className="nav-link">
          <FaUser /> Profile
        </NavLink>
      </nav>
    </div>
  );
}

export default Sidebar;