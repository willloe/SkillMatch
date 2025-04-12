import React, { useState } from "react";

function CareerIntent({ questions, onAllAnswered }) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState({});

  if (!questions || questions.length === 0) {
    return <div className="text-gray-500">No questions available.</div>;
  }

  const currentQuestion = questions[currentIndex];

  const handleSelect = (selectedOption) => {
    const updatedAnswers = {
      ...answers,
      [currentQuestion.question_text]: selectedOption,
    };

    setAnswers(updatedAnswers);

    if (currentIndex + 1 < questions.length) {
      setCurrentIndex(currentIndex + 1);
    } else {
      onAllAnswered(updatedAnswers);
    }
  };

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