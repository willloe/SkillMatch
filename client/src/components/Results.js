import React, { useState } from "react";
import JobCard from "./JobCard";

function Results({ recommendations = [], onSelectJob }) {
  const [selectedJob, setSelectedJob] = useState(null);

  const handleSelect = (jobTitle) => {
    setSelectedJob(jobTitle);
    onSelectJob(jobTitle); // send to backend or next step
  };

  const filteredJobs = selectedJob
    ? recommendations.filter((job) => job.title === selectedJob)
    : recommendations;

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4 text-center">
        {selectedJob ? "You selected:" : "Career Recommendations"}
      </h2>

      {recommendations.length === 0 && !selectedJob ? (
          <p>No recommendations available at this time.</p>
        ) : selectedJob ? (
          <JobCard job={selectedJob} isSelected={true} />
        ) : (
          <ul className="space-y-4">
            {recommendations.map((job, idx) => (
              <JobCard
                key={idx}
                job={job}
                onSelect={onSelectJob}
                isSelected={selectedJob?.title === job.title}
              />
            ))}
          </ul>
        )}
    </div>
  );
}

export default Results;
