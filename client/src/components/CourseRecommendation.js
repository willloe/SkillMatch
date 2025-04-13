import React from "react";
import JobCard from "./JobCard";

function CourseRecommendation({ job, skillGap = [], courses = [], programs = [] }) {
  if (!job) return null;

  return (
    <div className="max-w-xl mx-auto p-6">
      <h2 className="text-xl font-bold mb-4 text-green-700">🎯 Your Matched Career Path</h2>

      <JobCard job={job} showAction={true} expandable={true} />

      {skillGap.length > 0 && (
        <div className="mt-6">
            <h3 className="text-md font-semibold text-red-600 mb-2">🚧 Skill Gaps</h3>
            <div className="mt-3 flex flex-wrap gap-2">
            {skillGap.map((skill, idx) => (
                <span
                key={idx}
                className="bg-white border border-red-200 text-red-800 text-sm px-3 py-1 rounded-full shadow-sm"
                >
                {skill.trim()}
                </span>
            ))}
            </div>
        </div>
      )}

      {courses.length > 0 && (
        <div className="mt-6">
          <h3 className="text-md font-semibold text-blue-600 mb-2">📘 Recommended Courses</h3>
          <ul className="space-y-2">
            {courses.map((course, idx) => (
              <li key={idx} className="text-sm border p-3 rounded bg-gray-50">
                <strong>{course.title}</strong> — <a href={course.url} className="text-blue-500 underline" target="_blank" rel="noopener noreferrer">View</a>
                <p className="text-gray-600 mt-1">{course.summary}</p>
              </li>
            ))}
          </ul>
        </div>
      )}

      {programs.length > 0 && (
        <div className="mt-6">
          <h3 className="text-md font-semibold text-purple-600 mb-2">🎓 Recommended Degree Programs</h3>
          <ul className="space-y-2">
            {programs.map((program, idx) => (
              <li key={idx} className="text-sm border p-3 rounded bg-gray-50">
                <strong>{program.university}</strong> — {program.degree_level}
                <p className="text-gray-600">{program.cip_description}</p>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default CourseRecommendation;
