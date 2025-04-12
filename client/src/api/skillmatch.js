import axios from "axios";

const BASE_URL = "http://localhost:5000";

export const embedResume = async (text) => {
  const res = await axios.post(`${BASE_URL}/embed-resume`, { text });
  return res.data;
};