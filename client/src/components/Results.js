import React from "react";

function Results({ resume, results, intent }) {
  return (
    <div className="border p-4 rounded shadow space-y-4">
      <h2 className="text-xl font-semibold">Step 3: Results</h2>

      <div>
        <h3 className="font-semibold">Your Intent:</h3>
        <p>Career Goal: {intent.intent}</p>
        <p>Budget: {intent.budget}</p>
        <p>Time per week: {intent.time} hrs</p>
      </div>

      <div>
        <h3 className="font-semibold mt-4">Extracted Skills:</h3>
        <ul className="list-disc ml-6">
          {(results?.skills || []).map((skill, idx) => (
            <li key={idx}>{skill}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default Results;