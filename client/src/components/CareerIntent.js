import React, { useState } from "react";

function CareerIntent({ questions, onAllAnswered }) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [showSummary, setShowSummary] = useState(false);

  const currentQuestion = questions[currentIndex];

  const handleSelect = (selectedOption) => {
    const newAnswers = {
      ...answers,
      [currentQuestion.question_text]: selectedOption,
    };

    setAnswers(newAnswers);

    if (currentIndex + 1 < questions.length) {
      setCurrentIndex(currentIndex + 1);
    } else {
      setShowSummary(true);
      onAllAnswered(newAnswers);
    }
  };

  if (!questions || questions.length === 0) {
    return <div className="text-gray-500">No questions available.</div>;
  }

  if (showSummary) {
    return (
      <div className="space-y-4">
        {Object.entries(answers).map(([question, answer], idx) => (
          <details key={idx} className="mb-2 bg-white rounded border border-gray-200">
            <summary className="cursor-pointer py-2 px-4 font-semibold bg-gray-50 hover:bg-gray-100">
              {question}
            </summary>
            <div className="px-4 py-2 text-sm text-gray-800">{answer}</div>
          </details>
        ))}
      </div>
    );
  }

  return (
    <div className="max-w-xl mx-auto p-6">
      <h2 className="text-xl font-semibold mb-4">
        Question {currentIndex + 1} of {questions.length}
      </h2>
      <p className="mb-4 text-lg">{currentQuestion.question_text}</p>

      <div className="space-y-3">
        {currentQuestion.options.map((opt, idx) => (
          <button
            key={idx}
            className="block w-full text-left px-4 py-2 rounded bg-gray-100 hover:bg-blue-100 transition"
            onClick={() => handleSelect(opt)}
          >
            {opt}
          </button>
        ))}
      </div>
    </div>
  );
}

export default CareerIntent;