import React from "react";

function Results({ careerIntent, answers }) {
  const entries = Object.entries(answers);

  return (
    <div className="p-6 bg-white rounded shadow mt-4 max-w-xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Your Career Plan Summary</h2>

      <div className="mb-6">
        <h3 className="text-lg font-semibold">Your Selected Career Intent:</h3>
        <p className="text-blue-700 mt-2">{careerIntent}</p>
      </div>

      <div>
        <h3 className="text-lg font-semibold mb-2">Your Answers:</h3>
        <ul className="space-y-4">
          {entries.map(([question, answer], idx) => (
            <li key={idx} className="bg-gray-50 p-4 rounded shadow">
              <p className="font-medium mb-1">{question}</p>
              <p className="text-blue-600">{answer}</p>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default Results;
