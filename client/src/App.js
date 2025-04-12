import { useState } from "react";
import axios from "axios";

function App() {
  const [skills, setSkills] = useState([]);

  const testAPI = async () => {
    const res = await axios.post("http://localhost:5000/embed-resume", {
      text: "I have experience with Python, SQL, and Excel."
    });
    setSkills(res.data.skills);
  };

  return (
    <div>
      <h1>SkillMatch</h1>
      <button onClick={testAPI}>Analyze Resume</button>
      <ul>
        {skills.map((s, i) => <li key={i}>{s}</li>)}
      </ul>
    </div>
  );
}

export default App;