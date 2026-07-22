import { useState } from "react";
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
    <div className="upload-page">

      <h2>Upload Resume</h2>

      <form onSubmit={handleSubmit}>

        <label
          className="upload-box"
          onDrop={handleDrop}
          onDragOver={handleDragOver}
        >
          <input
            type="file"
            accept=".pdf,.doc,.docx"
            hidden
            onChange={handleFileChange}
          />

          <h3>📄 Drag & Drop Resume</h3>

          <p>or Click to Browse</p>

        </label>

        {file && (
          <p>
            <strong>Selected:</strong> {file.name}
          </p>
        )}

        <button type="submit" disabled={loading}> {loading ? "Uploading..." : "Upload Resume"} </button>

      </form>

      <p>{message}</p>

    </div>
  );
}

export default UploadResume;