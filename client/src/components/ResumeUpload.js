import React, { useState } from "react";

function ResumeUpload({ onComplete }) {
  const [uploading, setUploading] = useState(false);
  const [fileName, setFileName] = useState(null);

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setFileName(file.name);
    setUploading(true);

    const formData = new FormData();
    formData.append("resume", file);
    formData.append("user_id", "test_user"); // TODO: Replace with real user ID if needed

    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        console.error("❌ Upload failed:", data);
        alert(`Upload failed: ${data.error || 'Unknown error'}`);
        return;
      }

      if (data.success && onComplete) {
        let parsedQuestions = data.questions;
        if (typeof data.questions === "string") {
          try {
            parsedQuestions = JSON.parse(data.questions);
          } catch (err) {
            console.error("Failed to parse questions JSON:", err);
          }
        }
        
        console.log("📦 Response data:", data);
        // console.log("Questions data:", data.questions);
        // console.log("Parsed data:", parsedQuestions);

        const incomingQuestions = Array.isArray(parsedQuestions)
          ? parsedQuestions
          : [];

        // console.log("Questions data:", incomingQuestions);
        onComplete(incomingQuestions); // Pass up to SkillMatchFlow
      }
    } catch (err) {
      console.error("Upload error:", err);
      alert("Error uploading resume.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Upload Your Resume</h1>

      <input
        type="file"
        accept=".pdf,.txt"
        onChange={handleFileChange}
        className="mb-4 block w-full"
      />

      {uploading && <p className="text-blue-600 mb-4">Uploading & analyzing...</p>}
      {fileName && <p className="text-gray-600 mb-2">Uploaded: {fileName}</p>}
    </div>
  );
}

export default ResumeUpload;
