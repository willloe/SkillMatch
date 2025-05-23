# 🧠 SkillMatch

SkillMatch is an AI-powered career copilot designed to help users navigate career transitions. It provides:

- Resume analysis and structured skill extraction
- Career intent survey and profile summary
- Personalized job recommendations via Gemini + Pinecone
- Skill gap detection and tailored course/program recommendations

---

## 📦 Project Structure

```
SkillMatch/
├── client/           # React Frontend (Tailwind + SPA)
├── server/           # Flask Backend (API + Gemini + Pinecone)
├── vectorization/    # Vector embedding + Pinecone utilities (preprocessing, similarity search)
├── scraping/         # Webscraping logic using Firecrawl + Gemini for course data
└── README.md
```

---

## ⚙️ Setup Instructions

### 🔵 Frontend (React + Tailwind)

> Requires: Node.js v16+ and npm

1. Navigate to the frontend folder:

```bash
cd client
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm start
```

> App will run at `http://localhost:3000`

---

### 🔴 Backend (Flask + Python)

> Requires: Python 3.10+ and `pip`

1. Navigate to the backend folder:

```bash
cd server
```

2. Create and activate the virtual environment:

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. Run the Flask backend:

```bash
python run.py
```

> API will run at `http://localhost:5000`

---

## 🔐 Environment Variables

Create a `.env` file in `/server/` with your configuration:

```
GEMINI_API_KEY=your-gemini-api-key
PINECONE_API_KEY=your-pinecone-api-key
MONGODB_URI=your-mongodb-uri
GOOGLE_API_KEY=your-google-api-key
FIRECRAWL_API_KEY=your-firecrawl-api-key
```

---

## 📄 API Routes (Backend)

| Endpoint             | Method | Description                                        |
|----------------------|--------|----------------------------------------------------|
| `/upload`            | POST   | Upload and analyze resume                         |
| `/submit-answers`    | POST   | Submit career intent survey answers               |
| `/selected-job`      | POST   | Store selected job and return skill-based learning recommendations |

---

## 🛠️ Tech Stack

### Frontend
- React + Tailwind CSS
- File upload + dynamic steps UI
- Job card selection and course visualization

### Backend
- Flask + OpenAI Gemini API
- Pinecone vector search (job/course/program embeddings)
- MongoDB (user profiles + resume + survey)

### Vectorization Module
- Preprocesses job/course/program descriptions
- Generates Gemini embeddings
- Communicates with Pinecone for similarity search and indexing

### Scraping Module
- `webscraping.py` uses Firecrawl and Gemini APIs
- Extracts and structures online course data (e.g. from Udemy)

---

## 📚 Features

- Resume-to-skills pipeline (top + categorized skills)
- Gemini-generated survey & profile summary
- Smart matching to relevant jobs (Pinecone)
- Skill gap detection between job and user profile
- Learning recommendations (courses, academic programs)

---

## 🚀 Coming Soon

- Gemini fine-tuning with user feedback
- Exportable learning plans
- Live dashboard for career tracking
