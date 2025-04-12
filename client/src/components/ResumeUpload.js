import React, { useState } from "react";

function ResumeUpload({ onAnalyze }) {
  const [text, setText] = useState("");
  const [fileName, setFileName] = useState(null);
  const [loading, setLoading] = useState(false);

  const wordCount = text.trim().split(/\s+/).length;
  const isTextValid = wordCount >= 100;

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    setFileName(file.name);

    // Placeholder logic: you’d send this to backend to extract text
    const reader = new FileReader();
    reader.onload = (e) => {
      const fileText = e.target.result;
      setText(fileText); // Assume plaintext resume for now
    };
    reader.readAsText(file); // For .txt or .docx converted files
  };

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
    <div className="bg-white shadow-neumorphism rounded-xl p-6 space-y-4">
      <h2 className="text-xl font-semibold flex items-center gap-2">
        <span className="text-2xl">📄</span> Step 1: Upload Resume or Paste Text
      </h2>

      <div>
        <label className="block font-medium mb-1">Upload .pdf or .docx</label>
        <input
          type="file"
          accept=".pdf,.docx,.txt"
          className="block w-full"
          onChange={handleFileChange}
        />
        {fileName && <p className="text-sm text-gray-500 mt-1">Loaded: {fileName}</p>}
      </div>

      <div>
        <label className="block font-medium mb-1">Or paste your resume text</label>
        <textarea
          className="w-full h-40 p-3 rounded-xl border-none shadow-inner-neumorphism text-gray-700 focus:outline-none resize-none"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste or write your resume here (min. 100 words)..."
        />
        {!isTextValid && (
          <p className="text-red-500 text-sm mt-1">
            Resume text must be at least 100 words.
          </p>
        )}
      </div>

      <button
        onClick={handleAnalyze}
        className="bg-blue-600 hover:bg-blue-700 text-white font-medium px-6 py-2 rounded-xl transition shadow-neumorphism-button disabled:opacity-50"
        disabled={!isTextValid || loading}
      >
        {loading ? "Analyzing..." : "Analyze Resume"}
      </button>
    </div>
  );
}

export default ResumeUpload;