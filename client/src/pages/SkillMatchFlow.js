import React, { useState } from "react";
import ResumeUpload from "../components/ResumeUpload";
import CareerIntent from "../components/CareerIntent";
import Results from "../components/Results";

function SkillMatchFlow() {
  const [step, setStep] = useState(1);
  const [resumeText, setResumeText] = useState("");
  const [embeddingResult, setEmbeddingResult] = useState(null);
  const [intentData, setIntentData] = useState(null);

  return (
    <div className="max-w-2xl mx-auto p-6 space-y-8">
      <h1 className="text-3xl font-bold text-center">SkillMatch AI</h1>

      {step >= 1 && (
        <ResumeUpload
          onAnalyze={(resume, result) => {
            setResumeText(resume);
            setEmbeddingResult(result);
            setStep(2);
          }}
        />
      )}

      {step >= 2 && (
        <CareerIntent
          onNext={(intent) => {
            setIntentData(intent);
            setStep(3);
          }}
        />
      )}

      {step === 3 && embeddingResult && intentData && (
        <Results
          resume={resumeText}
          results={embeddingResult}
          intent={intentData}
        />
      )}
    </div>
  );
}

export default SkillMatchFlow;