import React, { useState } from "react";

function JobCard({ job, onSelect, isSelected, showAction = true, expandable = true }) {
  const [showDetails, setShowDetails] = useState(false);
  const [expanded, setExpanded] = useState(!expandable);

  const toggleDetails = () => setShowDetails((prev) => !prev);
  const toggleCard = () => setExpanded((prev) => !prev);

  return (
    <div
      className={`border rounded-xl shadow-md transition p-5 bg-white ${
        isSelected ? "border-blue-500 bg-blue-50" : "hover:border-gray-400"
      }`}
    >
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold">{job.title}</h3>
        {expandable && (
          <button
            className="text-sm text-blue-500 hover:underline"
            onClick={toggleCard}
          >
            {expanded ? "Collapse" : "Expand"}
          </button>
        )}
      </div>

      {expanded && (
        <>
          <p className="text-gray-600 text-sm mt-2 whitespace-pre-line">
            {showDetails || !expandable
              ? job.summary
              : job.summary.slice(0, 250) + "..."}
          </p>
          {expandable && job.summary.length > 250 && (
            <button
              onClick={toggleDetails}
              className="text-sm text-blue-500 mt-1 hover:underline"
            >
              {showDetails ? "Show less" : "Show more"}
            </button>
          )}

          {job.skills && (
            <div className="mt-3 flex flex-wrap gap-2">
              {typeof job.skills === "string"
                ? job.skills.split(",").map((skill, idx) => (
                    <span
                      key={idx}
                      className="bg-gray-100 text-sm px-2 py-1 rounded-full text-gray-700"
                    >
                      {skill.trim()}
                    </span>
                  ))
                : job.skills.map((skill, idx) => (
                    <span
                      key={idx}
                      className="bg-gray-100 text-sm px-2 py-1 rounded-full text-gray-700"
                    >
                      {skill.trim()}
                    </span>
                  ))}
            </div>
          )}

          {showAction && onSelect && (
            <button
              onClick={() => onSelect(job)}
              className="mt-4 px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700"
            >
              Select This Career
            </button>
          )}
        </>
      )}
    </div>
  );
}

export default JobCard;
