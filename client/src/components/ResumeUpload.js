import React, { useState } from "react";

function ResumeUpload({ onAnalyze }) {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!text.trim()) return;
    setLoading(true);
    try {
      // Simulate a delay
      await new Promise((res) => setTimeout(res, 1000));
  
      // Dummy response
      const mockResult = {
        skills: ["Python", "SQL", "Data Visualization", "Excel"],
      };
  
      onAnalyze(text, mockResult);
    } catch (err) {
      console.error("Mocked analysis failed:", err);
    } finally {
      setLoading(false);
    }
  };
  
  // const handleAnalyze = async () => {
  //   if (!text.trim()) return;
  //   setLoading(true);
  //   try {
  //     const res = await fetch("http://localhost:5000/embed-resume", {
  //       method: "POST",
  //       headers: { "Content-Type": "application/json" },
  //       body: JSON.stringify({ text }),
  //     });
  //     const data = await res.json();
  //     onAnalyze(text, data);
  //   } catch (err) {
  //     console.error("Analysis failed:", err);
  //   } finally {
  //     setLoading(false);
  //   }
  // };

  return (
    <div className="border p-4 rounded shadow space-y-4">
      <h2 className="text-xl font-semibold">Step 1: Upload Resume</h2>
      <textarea
        className="w-full h-32 p-2 border rounded"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Paste your resume here..."
      />
      <button
        onClick={handleAnalyze}
        className="bg-blue-600 text-white px-4 py-2 rounded"
        disabled={loading}
      >
        {loading ? "Analyzing..." : "Analyze Resume"}
      </button>
    </div>
  );
}

export default ResumeUpload;