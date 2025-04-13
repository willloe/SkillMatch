import axios from "axios";

const BASE_URL = "http://localhost:5000";

export const embedResume = async (text) => {
  const res = await axios.post(`${BASE_URL}/embed-resume`, { text });
  return res.data;
};

export async function submitSurveyAnswers(userId, answers) {
  try {
    const response = await fetch("http://localhost:5000/submit-answers", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id: userId,
        answers: answers,
      }),
    });

    const data = await response.json();
    return data;
  } catch (err) {
    console.error("❌ Error submitting answers:", err);
    throw err;
  }
}

export async function sendSelectedCareer(userId, selectedJob) {
  try {
    const response = await fetch("http://localhost:5000/selected-career", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, selected_job: selectedJob }),
    });

    const data = await response.json();
    if (!data.success) throw new Error(data.error || "Failed to save selection.");
    return data;
  } catch (err) {
    console.error("❌ Error sending selected job:", err);
    throw err;
  }
}