import React, { useState } from "react";
import ResumeUpload from "../components/ResumeUpload";
import StepIndicator from "../components/StepIndicator";
import StepWrapper from "../components/StepWrapper";
import CareerIntent from "../components/CareerIntent";
import Results from "../components/Results";
import { submitSurveyAnswers } from "../api/skillmatch";

function SkillMatchFlow() {
  const [step, setStep] = useState(1);
  const [questions, setQuestions] = useState([]);
  const [allAnswers, setAllAnswers] = useState({});
  const [careerIntent, setCareerIntent] = useState(null);
  const [recommendations, setRecommendations] = useState([]);

  const handleUploadComplete = (incomingQuestions) => {
    setQuestions(incomingQuestions);
    setStep(2);
  };

  const handleSurveyComplete = async (selectedAnswers) => {
    setAllAnswers(selectedAnswers);
    try {
      const userId = "test_user"; // Replace with dynamic user ID logic if needed
      const result = await submitSurveyAnswers(userId, selectedAnswers);
      console.log("✅ Backend response:", result);

      if (result.recommendations) {
        setRecommendations(result.recommendations);
      }

      setStep(3);
    } catch (error) {
      console.error("❌ Failed to submit survey:", error);
      alert("Something went wrong while submitting your answers.");
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 space-y-8">
      <h1 className="text-3xl font-bold text-center">SkillMatch AI</h1>
      <StepIndicator current={step} /> 
      <StepWrapper visible={step >= 1}>
        <ResumeUpload onComplete={handleUploadComplete} />
      </StepWrapper>
      <StepWrapper visible={step >= 2}>
      <CareerIntent
        questions={questions}
        onAllAnswered={handleSurveyComplete}
      />
      </StepWrapper>
      <StepWrapper visible={step === 3}>
      <Results
          careerIntent={careerIntent}
          answers={allAnswers}
      />
      </StepWrapper>
    </div>
  );
}

export default SkillMatchFlow;