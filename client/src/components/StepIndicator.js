import React from "react";

function StepIndicator({ current }) {
  const steps = ["Upload Resume", "Career Survey", "Results"];
  const progress = ((current - 1) / (steps.length - 1)) * 100;

  return (
    <div className="w-full max-w-2xl mx-auto mb-8 px-4">
      {/* Progress Track */}
      <div className="relative w-full h-3 bg-gray-300 rounded-full shadow-inner overflow-hidden">
        <div
          className="absolute left-0 top-0 bottom-0 bg-blue-500 rounded-full transition-all duration-300"
          style={{ width: `${progress}%` }}
        ></div>
      </div>
      {/* Step Labels */}
      <div className="mt-2 flex justify-between text-xs text-gray-600">
        {steps.map((label, idx) => (
          <div
            key={idx}
            className={`text-center flex-1 ${
              current === idx + 1 ? "text-blue-700 font-semibold" : ""
            }`}
          >
            {label}
          </div>
        ))}
      </div>
    </div>
  );
}
  
export default StepIndicator;