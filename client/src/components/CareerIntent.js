import React, { useState } from "react";

function CareerIntent({ questions, onAllAnswered }) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState({});

  const currentQuestion = questions[currentIndex];

  const handleSelect = (selectedOption) => {
    const newAnswers = {
      ...answers,
      [currentQuestion.text]: selectedOption,
    };

    setAnswers(newAnswers);

    if (currentIndex + 1 < questions.length) {
      setCurrentIndex(currentIndex + 1);
    } else {
      // Done!
      onAllAnswered(newAnswers);
    }
  };

  if (!currentQuestion) return null;

  return (
    <div className="p-6 bg-white rounded shadow mt-4 max-w-xl mx-auto">
      <h2 className="text-lg font-bold mb-4">Question {currentIndex + 1} of {questions.length}</h2>
      <p className="text-md font-semibold mb-3">{currentQuestion.text}</p>

      <div className="space-y-2">
        {currentQuestion.options.map((opt, idx) => (
          <button
            key={idx}
            onClick={() => handleSelect(opt)}
            className="block w-full text-left px-4 py-2 bg-blue-50 hover:bg-blue-100 rounded"
          >
            {opt}
          </button>
        ))}
      </div>
    </div>
  );
}

export default CareerIntent;