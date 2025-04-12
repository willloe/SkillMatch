import os
import json
from dotenv import load_dotenv
from google.generativeai import GenerativeModel, configure
import google.generativeai as genai
from pymongo import MongoClient
from bson.objectid import ObjectId

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Configure Gemini API
if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY")
configure(api_key=GEMINI_API_KEY)

# Models
embedding_model = GenerativeModel('models/text-embedding-004')
text_generation_model = GenerativeModel('gemini-1.5-flash-latest')

# MongoDB
client = MongoClient(os.getenv('MONGODB_URI'))
db = client['skillmatch_db']
profiles_collection = db['profiles']

def extract_top_skills(resume_text):
    prompt = f"""
    You are a resume analysis assistant.

    Analyze the resume below and extract the **top 5 most relevant professional skills** the candidate demonstrates — across **any domain**, such as:

    - Communication
    - Problem-solving
    - Leadership
    - Data analysis
    - Project management
    - Creativity
    - Strategic thinking
    - Customer service
    - Conflict resolution
    - Team collaboration

    Avoid focusing solely on programming languages or technical tools. Instead, return **broad, high-level skills** that reflect the person’s core strengths and work capabilities.

    Return your output as a **JSON list of strings**, for example:
    ["Communication", "Project Management", "Team Collaboration", "Problem Solving", "Creativity"]

    Resume:
    --- START RESUME ---
    {resume_text}
    --- END RESUME ---
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        raw_text = response.text.strip().lstrip("```json").rstrip("```").strip()
        skills = json.loads(raw_text)
        return skills
    except Exception as e:
        print("❌ Skill extraction failed:", e)
        return []

def extract_categorized_skills(resume_text):
    import pandas as pd
    import random

    csv_path = os.path.join("app", "prompts", "skills.csv")
    skills_df = pd.read_csv(csv_path)

    # Sample up to 20 diverse skills per domain
    domain_instruction = ""
    for domain, group in skills_df.groupby("Domain"):
        sampled = random.sample(list(group["Element Name"]), min(20, len(group)))
        domain_instruction += f"- {domain}: {', '.join(sampled)}...\n"

    prompt = f"""
    You are a career assistant that analyzes resumes and maps them to structured occupational skill categories.

    Based on the resume below, match relevant content to the following skills grouped by domain:

    {domain_instruction}

    Return a JSON object like:
    {{
    "Abilities": [...],
    "Knowledge": [...],
    ...
    }}
    Resume Text:
    --- START RESUME ---
    {resume_text}
    --- END RESUME ---
    """
    
    # Gemini generation logic (same pattern as generate_mcqs)
    generation_config = genai.types.GenerationConfig(
        temperature=0.5,
        max_output_tokens=2048
    )

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]

    response = text_generation_model.generate_content(
        prompt,
        generation_config=generation_config,
        safety_settings=safety_settings
    )

    if not response.parts:
        block_reason = getattr(response.prompt_feedback, 'block_reason', 'Unknown')
        raise ValueError(f"Structured skill response was blocked or empty. Reason: {block_reason}")

    try:
        cleaned_json = response.text.strip().lstrip("```json\n").rstrip("```").strip()
        skills_by_category = json.loads(cleaned_json)

        if isinstance(skills_by_category, dict):
            return skills_by_category

        raise ValueError("Gemini did not return a valid skills JSON object.")

    except json.JSONDecodeError as e:
        print("❌ Structured skills parse error:", response.text)
        raise ValueError("Gemini returned invalid structured skills JSON.")

def generate_and_store_embeddings(text, user_id, top_skills=[], structured_skills={}):
    try:
        response = genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="retrieval_document"
        )
        embeddings = response['embedding']

        profile_data = {
            'user_id': user_id,
            'embeddings': embeddings,
            'top_skills': top_skills,
            'structured_skills': structured_skills
        }

        result = profiles_collection.insert_one(profile_data)
        return result.inserted_id

    except Exception as e:
        raise ValueError(f"Error generating embeddings: {e}")

def generate_mcq_survey_prompt(resume_text, top_skills=[], structured_skills={}):
    # Format structured_skills for the prompt
    structured_summary = "\n".join([
        f"- {domain}: {', '.join(skills) if skills else 'None detected'}"
        for domain, skills in structured_skills.items()
    ])

    skills_snippet = f"The top 3 skills extracted were: {', '.join(top_skills[:3])}." if top_skills else ""

    prompt = f"""
    You are a career advisor AI helping someone discover their next step in work and learning.

    Their resume has been analyzed. Now, generate **10 multiple-choice questions** that will:
    1. Uncover their **motivation, budget, and aspirations** (first 3 questions)
    2. Identify **gaps or preferences** in their work style, skills, or knowledge (last 7 questions)

    ---

    ### RESUME SUMMARY:
    {skills_snippet}

    ### STRUCTURED SKILLS EXTRACTED:
    {structured_summary}

    ---

    ### QUESTION FORMAT:
    Return a JSON list like:
    [
    {{
        "question_text": "What is your dream job or title?",
        "options": ["A) Data Scientist", "B) Software Engineer", "C) Product Manager", "D) Not sure"]
    }},
    ...
    ]

    ### INSTRUCTIONS:
    - Questions 1–3 must focus on career **intent, dream company, job title, learning budget, or motivation**.
    - Questions 4–10 must explore **missing dimensions** from the resume, such as:
    - Skills not mentioned
    - Learning style (online vs in-person)
    - Ideal job environment (hybrid, remote)
    - Work values or preferences
    - Keep each question clear, friendly, and answerable regardless of their experience level.
    - Use resume-based context to personalize, but feel free to ask broad questions too.

    ---

    ### Resume Text:
    --- START RESUME ---
    {resume_text}
    --- END RESUME ---
    """
    return prompt

def generate_mcqs(resume_text, top_skills=[], structured_skills={}):
    prompt = generate_mcq_survey_prompt(resume_text, top_skills, structured_skills)
    generation_config = genai.types.GenerationConfig(
        temperature=0.5,
        max_output_tokens=2048
    )

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]

    response = text_generation_model.generate_content(
        prompt,
        generation_config=generation_config,
        safety_settings=safety_settings
    )

    if not response.parts:
        block_reason = getattr(response.prompt_feedback, 'block_reason', 'Unknown')
        raise ValueError(f"Response was blocked or empty. Reason: {block_reason}")

    try:
        cleaned_json = response.text.strip().lstrip("```json\n").rstrip("```")
        questions = json.loads(cleaned_json)
        if isinstance(questions, list) and len(questions) == 10:
            return questions
        raise ValueError("Gemini did not return 10 valid MCQs.")
    except json.JSONDecodeError:
        raise ValueError("Gemini returned invalid JSON.")
