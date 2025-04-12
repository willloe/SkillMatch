import React from "react";

function Results({ resume, results, intent }) {
  return (
    <div className="bg-white shadow-neumorphism rounded-xl p-6 space-y-4">
      <h2 className="text-xl font-semibold flex items-center gap-2">
        <span className="text-2xl">📊</span> Step 3: Results
      </h2>

      <div className="space-y-2">
        <h3 className="font-semibold">Your Intent:</h3>
        <p><strong>Career Goal:</strong> {intent.intent}</p>
        <p><strong>Budget:</strong> {intent.budget}</p>
        <p><strong>Time per week:</strong> {intent.time} hrs</p>
      </div>

      <div>
        <h3 className="font-semibold mt-4">Extracted Skills:</h3>
        <ul className="list-disc ml-6 text-gray-800">
          {(results?.skills || []).map((skill, idx) => (
            <li key={idx}>{skill}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default Results;