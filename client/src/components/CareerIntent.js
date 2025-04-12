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
    <div className="bg-white shadow-neumorphism rounded-xl p-6 space-y-4">
      <h2 className="text-xl font-semibold flex items-center gap-2">
        <span className="text-2xl">🎯</span> Step 2: Career Intent
      </h2>

      <div className="space-y-2">
        <label className="font-semibold block">What is your career goal?</label>
        <select
          className="w-full p-2 rounded-xl shadow-inner-neumorphism border-none focus:outline-none"
          value={intent}
          onChange={(e) => setIntent(e.target.value)}
        >
          <option value="">Select...</option>
          <option value="upskill">Upskill in current job</option>
          <option value="switch">Switch to a new career</option>
          <option value="explore">Just exploring</option>
        </select>
      </div>

      <div className="space-y-2">
        <label className="font-semibold block">What’s your budget for learning?</label>
        <select
          className="w-full p-2 rounded-xl shadow-inner-neumorphism border-none focus:outline-none"
          value={budget}
          onChange={(e) => setBudget(e.target.value)}
        >
          <option value="">Select...</option>
          <option value="free">Free only</option>
          <option value="low">Under $100</option>
          <option value="any">Flexible</option>
        </select>
      </div>

      <div className="space-y-2">
        <label className="font-semibold block">Hours/week you can commit:</label>
        <input
          className="w-full p-2 rounded-xl shadow-inner-neumorphism border-none focus:outline-none"
          type="number"
          value={time}
          onChange={(e) => setTime(e.target.value)}
          placeholder="e.g., 5"
        />
      </div>

      <button
        onClick={handleSubmit}
        className="mt-4 bg-green-600 hover:bg-green-700 text-white font-medium px-6 py-2 rounded-xl transition shadow-neumorphism-button"
      >
        Continue
      </button>
    </div>
  );
}

export default CareerIntent;
