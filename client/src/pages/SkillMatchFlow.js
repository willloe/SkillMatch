import React, { useState } from "react";
import ResumeUpload from "../components/ResumeUpload";
import StepIndicator from "../components/StepIndicator";
import StepWrapper from "../components/StepWrapper";
import CareerIntent from "../components/CareerIntent";
import Results from "../components/Results";

function SkillMatchFlow() {
  const [step, setStep] = useState(1);
  const [questions, setQuestions] = useState([]);
  const [allAnswers, setAllAnswers] = useState({});
  const [careerIntent, setCareerIntent] = useState(null);

  return (
    <div className="max-w-2xl mx-auto p-6 space-y-8">
      <h1 className="text-3xl font-bold text-center">SkillMatch AI</h1>
      <StepIndicator current={step} /> 
      <StepWrapper visible={step >= 1}>
        <ResumeUpload
          onComplete={(questions) => {
            setQuestions(questions); // pass from child up to SkillMatchFlow
            setStep(2);
          }}
        />
      </StepWrapper>
      <StepWrapper visible={step >= 2}>
      <CareerIntent
        questions={questions}
        onAllAnswered={(answers) => {
          setCareerIntent(answers["What is your career aspiration?"] || "Unspecified");
          setAllAnswers(answers); // If you want to track all
          setStep(3);
        }}
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