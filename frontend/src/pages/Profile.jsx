import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import DashboardLayout from "../layouts/DashboardLayout";
import { FaUser, FaEnvelope, FaPhone, FaMapMarkerAlt, FaBriefcase, FaEdit, FaSave, FaTimes, FaMoon, FaSun, FaSignOutAlt, FaSpinner } from "react-icons/fa";
import { getUserProfile, updateUserProfile } from "../services/userService";

function Profile() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [theme, setTheme] = useState("light");

  // Form state
  const [formData, setFormData] = useState({
    full_name: "",
    email: "",
    phone: "",
    location: "",
    professional_title: "",
    skills: "",
  });

  const [formErrors, setFormErrors] = useState({});

  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        setLoading(true);
        const data = await getUserProfile();
        setUser(data);
        setFormData({
          full_name: data.full_name || "",
          email: data.email || "",
          phone: data.phone || "",
          location: data.location || "",
          professional_title: data.professional_title || "",
          skills: data.skills || "",
        });
        
        // Load theme preference
        const savedTheme = localStorage.getItem("theme") || "light";
        setTheme(savedTheme);
      } catch (err) {
        setError("Failed to load profile");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchUserProfile();
  }, []);

  const validateForm = () => {
    const errors = {};
    
    if (!formData.full_name.trim()) {
      errors.full_name = "Name is required";
    } else if (formData.full_name.length < 2) {
      errors.full_name = "Name must be at least 2 characters";
    } else if (formData.full_name.length > 100) {
      errors.full_name = "Name must be less than 100 characters";
    }
    
    if (!formData.email.trim()) {
      errors.email = "Email is required";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      errors.email = "Invalid email format";
    }
    
    if (formData.phone && formData.phone.length > 20) {
      errors.phone = "Phone number must be less than 20 characters";
    }
    
    if (formData.location && formData.location.length > 100) {
      errors.location = "Location must be less than 100 characters";
    }
    
    if (formData.professional_title && formData.professional_title.length > 100) {
      errors.professional_title = "Professional title must be less than 100 characters";
    }
    
    if (formData.skills && formData.skills.length > 500) {
      errors.skills = "Skills must be less than 500 characters";
    }
    
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    // Clear error for this field when user starts typing
    if (formErrors[name]) {
      setFormErrors({ ...formErrors, [name]: "" });
    }
  };

  const handleSave = async () => {
    if (!validateForm()) {
      return;
    }

    try {
      setSaving(true);
      setError("");
      setSuccess("");
      
      const updatedUser = await updateUserProfile(formData);
      setUser(updatedUser);
      setIsEditing(false);
      setSuccess("Profile updated successfully!");
      
      // Clear success message after 3 seconds
      setTimeout(() => setSuccess(""), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to update profile");
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    if (user) {
      setFormData({
        full_name: user.full_name || "",
        email: user.email || "",
        phone: user.phone || "",
        location: user.location || "",
        professional_title: user.professional_title || "",
        skills: user.skills || "",
      });
    }
    setIsEditing(false);
    setFormErrors({});
    setError("");
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  const toggleTheme = () => {
    const newTheme = theme === "light" ? "dark" : "light";
    setTheme(newTheme);
    localStorage.setItem("theme", newTheme);
    // Apply theme to document
    if (newTheme === "dark") {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="max-w-3xl mx-auto py-8">
          <div className="flex items-center gap-2 text-slate-600 dark:text-slate-400">
            <FaSpinner className="animate-spin" />
            <span>Loading profile...</span>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  if (error && !user) {
    return (
      <DashboardLayout>
        <div className="max-w-3xl mx-auto py-8">
          <div className="bg-rose-50 dark:bg-rose-900/30 border border-rose-200 dark:border-rose-900/50 rounded-lg p-6">
            <p className="text-rose-700 dark:text-rose-400 font-medium">{error}</p>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="max-w-3xl mx-auto py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Profile Settings</h1>
          <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">
            Manage your account information and preferences
          </p>
        </div>

        {/* Success Message */}
        {success && (
          <div className="mb-6 bg-emerald-50 dark:bg-emerald-900/30 border border-emerald-200 dark:border-emerald-900/50 rounded-lg p-4">
            <p className="text-sm text-emerald-700 dark:text-emerald-400">{success}</p>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="mb-6 bg-rose-50 dark:bg-rose-900/30 border border-rose-200 dark:border-rose-900/50 rounded-lg p-4">
            <p className="text-sm text-rose-700 dark:text-rose-400">{error}</p>
          </div>
        )}

        {/* Profile Card */}
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm p-6 mb-6">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-4">
              <div className="h-16 w-16 rounded-full bg-indigo-100 dark:bg-indigo-900/40 flex items-center justify-center text-indigo-600 dark:text-indigo-400 text-2xl font-bold">
                {user?.full_name?.charAt(0).toUpperCase() || "U"}
              </div>
              <div>
                <h2 className="text-lg font-semibold text-slate-900 dark:text-white">
                  {user?.full_name || "User"}
                </h2>
                <p className="text-sm text-slate-500 dark:text-slate-400">
                  {user?.email || "user@example.com"}
                </p>
              </div>
            </div>
            {!isEditing && (
              <button
                onClick={() => setIsEditing(true)}
                className="px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-lg hover:bg-indigo-700 transition-colors flex items-center gap-2"
              >
                <FaEdit />
                Edit Profile
              </button>
            )}
          </div>

          {/* Profile Form */}
          {isEditing ? (
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                  Full Name *
                </label>
                <input
                  type="text"
                  name="full_name"
                  value={formData.full_name}
                  onChange={handleInputChange}
                  className={`w-full px-4 py-2 border rounded-lg bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent ${
                    formErrors.full_name ? "border-rose-500" : "border-slate-300 dark:border-slate-700"
                  }`}
                  placeholder="Enter your full name"
                />
                {formErrors.full_name && (
                  <p className="mt-1 text-xs text-rose-600 dark:text-rose-400">{formErrors.full_name}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                  Email *
                </label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  className={`w-full px-4 py-2 border rounded-lg bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent ${
                    formErrors.email ? "border-rose-500" : "border-slate-300 dark:border-slate-700"
                  }`}
                  placeholder="Enter your email"
                />
                {formErrors.email && (
                  <p className="mt-1 text-xs text-rose-600 dark:text-rose-400">{formErrors.email}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                  Phone
                </label>
                <input
                  type="text"
                  name="phone"
                  value={formData.phone}
                  onChange={handleInputChange}
                  className={`w-full px-4 py-2 border rounded-lg bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent ${
                    formErrors.phone ? "border-rose-500" : "border-slate-300 dark:border-slate-700"
                  }`}
                  placeholder="Enter your phone number"
                />
                {formErrors.phone && (
                  <p className="mt-1 text-xs text-rose-600 dark:text-rose-400">{formErrors.phone}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                  Location
                </label>
                <input
                  type="text"
                  name="location"
                  value={formData.location}
                  onChange={handleInputChange}
                  className={`w-full px-4 py-2 border rounded-lg bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent ${
                    formErrors.location ? "border-rose-500" : "border-slate-300 dark:border-slate-700"
                  }`}
                  placeholder="Enter your location"
                />
                {formErrors.location && (
                  <p className="mt-1 text-xs text-rose-600 dark:text-rose-400">{formErrors.location}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                  Professional Title
                </label>
                <input
                  type="text"
                  name="professional_title"
                  value={formData.professional_title}
                  onChange={handleInputChange}
                  className={`w-full px-4 py-2 border rounded-lg bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent ${
                    formErrors.professional_title ? "border-rose-500" : "border-slate-300 dark:border-slate-700"
                  }`}
                  placeholder="e.g., Software Engineer, Data Scientist"
                />
                {formErrors.professional_title && (
                  <p className="mt-1 text-xs text-rose-600 dark:text-rose-400">{formErrors.professional_title}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                  Skills
                </label>
                <textarea
                  name="skills"
                  value={formData.skills}
                  onChange={handleInputChange}
                  rows="3"
                  className={`w-full px-4 py-2 border rounded-lg bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent ${
                    formErrors.skills ? "border-rose-500" : "border-slate-300 dark:border-slate-700"
                  }`}
                  placeholder="List your skills separated by commas (e.g., Python, React, SQL)"
                />
                {formErrors.skills && (
                  <p className="mt-1 text-xs text-rose-600 dark:text-rose-400">{formErrors.skills}</p>
                )}
              </div>

              <div className="flex gap-3 pt-4">
                <button
                  onClick={handleSave}
                  disabled={saving}
                  className="flex items-center gap-2 px-6 py-2 bg-emerald-600 text-white font-medium rounded-lg hover:bg-emerald-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {saving ? <FaSpinner className="animate-spin" /> : <FaSave />}
                  {saving ? "Saving..." : "Save Changes"}
                </button>
                <button
                  onClick={handleCancel}
                  disabled={saving}
                  className="flex items-center gap-2 px-6 py-2 bg-slate-600 text-white font-medium rounded-lg hover:bg-slate-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <FaTimes />
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="flex items-start gap-3">
                <FaUser className="text-slate-400 mt-1" />
                <div>
                  <p className="text-sm text-slate-500 dark:text-slate-400">Full Name</p>
                  <p className="text-base font-medium text-slate-900 dark:text-white">
                    {user?.full_name || "Not set"}
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <FaEnvelope className="text-slate-400 mt-1" />
                <div>
                  <p className="text-sm text-slate-500 dark:text-slate-400">Email</p>
                  <p className="text-base font-medium text-slate-900 dark:text-white">
                    {user?.email || "Not set"}
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <FaPhone className="text-slate-400 mt-1" />
                <div>
                  <p className="text-sm text-slate-500 dark:text-slate-400">Phone</p>
                  <p className="text-base font-medium text-slate-900 dark:text-white">
                    {user?.phone || "Not set"}
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <FaMapMarkerAlt className="text-slate-400 mt-1" />
                <div>
                  <p className="text-sm text-slate-500 dark:text-slate-400">Location</p>
                  <p className="text-base font-medium text-slate-900 dark:text-white">
                    {user?.location || "Not set"}
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <FaBriefcase className="text-slate-400 mt-1" />
                <div>
                  <p className="text-sm text-slate-500 dark:text-slate-400">Professional Title</p>
                  <p className="text-base font-medium text-slate-900 dark:text-white">
                    {user?.professional_title || "Not set"}
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <FaBriefcase className="text-slate-400 mt-1" />
                <div>
                  <p className="text-sm text-slate-500 dark:text-slate-400">Skills</p>
                  <p className="text-base font-medium text-slate-900 dark:text-white">
                    {user?.skills || "Not set"}
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Settings Card */}
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm p-6 mb-6">
          <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-4">Settings</h3>
          
          <div className="space-y-4">
            {/* Theme Toggle */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                {theme === "light" ? <FaSun className="text-amber-500" /> : <FaMoon className="text-indigo-400" />}
                <div>
                  <p className="text-sm font-medium text-slate-900 dark:text-white">Theme</p>
                  <p className="text-xs text-slate-500 dark:text-slate-400">
                    {theme === "light" ? "Light mode" : "Dark mode"}
                  </p>
                </div>
              </div>
              <button
                onClick={toggleTheme}
                className="px-4 py-2 bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 text-sm font-medium rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
              >
                Toggle
              </button>
            </div>

            {/* Account Info */}
            <div className="pt-4 border-t border-slate-200 dark:border-slate-700">
              <p className="text-sm text-slate-500 dark:text-slate-400 mb-2">Account Information</p>
              <div className="space-y-1 text-xs text-slate-600 dark:text-slate-400">
                <p>Role: {user?.role || "User"}</p>
                <p>Status: {user?.is_active ? "Active" : "Inactive"}</p>
                <p>Member since: {user?.created_at ? new Date(user.created_at).toLocaleDateString() : "Unknown"}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Logout Button */}
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl shadow-sm p-6">
          <button
            onClick={handleLogout}
            className="w-full flex items-center justify-center gap-2 px-6 py-3 bg-rose-600 text-white font-medium rounded-lg hover:bg-rose-700 transition-colors"
          >
            <FaSignOutAlt />
            Logout
          </button>
        </div>
      </div>
    </DashboardLayout>
  );
}

export default Profile;
