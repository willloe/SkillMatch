import React, { useState } from "react";

function CareerIntent({ onNext }) {
  const [intent, setIntent] = useState("");
  const [budget, setBudget] = useState("");
  const [time, setTime] = useState("");

  const handleSubmit = () => {
    if (!intent || !budget || !time) return;
    onNext({ intent, budget, time });
  };

  return (
    <div className="border p-4 rounded shadow space-y-4">
      <h2 className="text-xl font-semibold">Step 2: Career Intent</h2>

      <div>
        <label className="font-semibold">What is your career goal?</label>
        <select
          className="block w-full border rounded p-2 mt-1"
          value={intent}
          onChange={(e) => setIntent(e.target.value)}
        >
          <option value="">Select...</option>
          <option value="upskill">Upskill in current job</option>
          <option value="switch">Switch to a new career</option>
          <option value="explore">Just exploring</option>
        </select>
      </div>

      <div>
        <label className="font-semibold">What’s your budget for learning?</label>
        <select
          className="block w-full border rounded p-2 mt-1"
          value={budget}
          onChange={(e) => setBudget(e.target.value)}
        >
          <option value="">Select...</option>
          <option value="free">Free only</option>
          <option value="low">Under $100</option>
          <option value="any">Flexible</option>
        </select>
      </div>

      <div>
        <label className="font-semibold">Hours/week you can commit:</label>
        <input
          className="w-full border rounded p-2 mt-1"
          type="number"
          value={time}
          onChange={(e) => setTime(e.target.value)}
          placeholder="e.g., 5"
        />
      </div>

      <button
        onClick={handleSubmit}
        className="mt-4 bg-green-600 text-white px-4 py-2 rounded"
      >
        Continue
      </button>
    </div>
  );
}

export default CareerIntent;
