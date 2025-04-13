import React, { useState, useEffect, useRef } from "react";
import ResumeUpload from "../components/ResumeUpload";
import StepIndicator from "../components/StepIndicator";
import StepWrapper from "../components/StepWrapper";
import CareerIntent from "../components/CareerIntent";
import Results from "../components/Results";
import CourseRecommendation from "../components/CourseRecommendation";
import { submitSurveyAnswers, sendSelectedCareer  } from "../api/skillmatch";
import { getUserId } from "../utils/user";

function SkillMatchFlow() {
  const [step, setStep] = useState(1);
  const [questions, setQuestions] = useState([]);
  const [selectedJob, setSelectedJob] = useState(null);
  const [allAnswers, setAllAnswers] = useState({});
  const [courseData, setCourseData] = useState(null);
  const skillGap = courseData?.skillGap || [];
  const courseRecommendations = courseData?.recommendedCourses || [];
  const programRecommendations = courseData?.recommendedPrograms || [];
  const [jobRecommendations, setJobRecommendations] = useState([]);
  const stepRefs = [
    useRef(null),
    useRef(null),
    useRef(null),
    useRef(null),
  ];

  useEffect(() => {
    const target = stepRefs[step - 1]?.current; // Step is 1-indexed, array is 0-indexed
    if (target) {
      window.scrollTo({
        top: target.getBoundingClientRect().top + window.scrollY - 60, // Adjust for header height if needed
        behavior: "smooth",
      });
    }
  }, [step]);

  const handleUploadComplete = (incomingQuestions) => {
    setQuestions(incomingQuestions);
    setStep(2);
  };

  const handleSurveyComplete = async (selectedAnswers) => {
    setAllAnswers(selectedAnswers);
    try {
      const userId = getUserId();  
      const result = await submitSurveyAnswers(userId, selectedAnswers);
      console.log("✅ Backend response:", result);
      if (result.recommendations) {
        console.log(result.recommendations)
        setJobRecommendations(result.recommendations);
      }
      setStep(3);
    } catch (error) {
      console.error("❌ Failed to submit survey:", error);
      alert("Something went wrong while submitting your answers.");
    }
  };

  const handleCareerSelected = async (job) => {
    try {
      const response = await fetch("http://localhost:5000/selected-job", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ user_id: getUserId(), selected_job: job }),
      });
  
      const data = await response.json();
      console.log("✅ Career selection saved:", data);
  
      if (data.success) {
        setSelectedJob(job);
        setCourseData({
          skillGap: data.skill_gap,
          recommendedCourses: data.recommended_courses,
          recommendedPrograms: data.recommended_programs,
        });
        setStep(4); // ⬅️ Only if you want to move to step 4 after job selection
      } else {
        console.error("❌ Backend returned error:", data.error);
      }
    } catch (err) {
      console.error("❌ Failed to submit selected job:", err);
    }
  };


  return (
    <div className="max-w-2xl mx-auto p-6 space-y-8">
      <h1 className="text-3xl font-bold text-center">SkillMatch AI</h1>
      <StepIndicator current={step} /> 
      <StepWrapper visible={step >= 1} ref={stepRefs[0]}>
        <ResumeUpload onComplete={handleUploadComplete} />
      </StepWrapper>
      <StepWrapper visible={step >= 2} ref={stepRefs[1]}>
      <CareerIntent
        questions={questions}
        onAllAnswered={handleSurveyComplete}
      />
      </StepWrapper>
      <StepWrapper visible={step === 3} ref={stepRefs[2]}>
      <Results
        recommendations={jobRecommendations}
        onSelectJob={handleCareerSelected}
      />
      </StepWrapper>
      <StepWrapper visible={selectedJob && courseRecommendations} ref={stepRefs[3]}>
      <CourseRecommendation
        job={selectedJob}
        skillGap={skillGap}
        courses={courseRecommendations}
        programs={programRecommendations}
      />
      </StepWrapper>
    </div>
  );
}

export default SkillMatchFlow;