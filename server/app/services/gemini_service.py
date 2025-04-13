from collections import defaultdict
import os
import json
import pandas as pd
from dotenv import load_dotenv
from google.generativeai import GenerativeModel, configure
import google.generativeai as genai

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Configure Gemini API
if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY")
configure(api_key=GEMINI_API_KEY)

skills_csv_path = os.path.join("app", "prompts", "skills.csv")
skills_df = pd.read_csv(skills_csv_path)

# Group by domain
skill_domains = defaultdict(list)
for _, row in skills_df.iterrows():
    skill_domains[row["Domain"]].append(row["Element Name"].strip())

# Now create prompt-compatible string
domain_instruction = ""
for domain, skills in skill_domains.items():
    quoted_skills = ', '.join([f'"{skill}"' for skill in skills])
    domain_instruction += f'"{domain}": [{quoted_skills}]\n'

# Models
text_generation_model = GenerativeModel('gemini-1.5-flash-latest')

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
        print("Skill extraction failed:", e)
        return []

def extract_categorized_skills(resume_text):
    prompt = f"""
    You are a career assistant AI that analyzes resumes and maps the candidate’s experience to structured occupational skills.
    You MUST select skills only from the following predefined domain buckets (based on O*NET taxonomy):
    {domain_instruction}
    ---
    Task:
    - Read the candidate’s resume.
    - Identify all relevant skills they appear to demonstrate.
    - Categorize those skills under the appropriate domains above.
    - ONLY include skills from the list above. DO NOT invent or generalize new skills.

    Return your answer as a JSON object with this structure:
    {{
    "Abilities": [...],
    "Knowledge": [...],
    "Skills": [...],
    "Work Activities": [...],
    "Work Context": [...],
    "Work Styles": [...],
    "Work Values": [...]
    }}

    Resume:
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
        print("Structured skills parse error:", response.text)
        raise ValueError("Gemini returned invalid structured skills JSON.")

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
    1. Uncover their **motivation, budget, time, and aspirations** (first 4 questions)
    2. Identify **gaps or preferences** in their work style, skills, or knowledge (last 6 questions)

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
    - Questions 1–4 must focus on career **intent, dream company, job title, learning budget, learning time, or motivation**.
    - Questions 5–10 must explore **missing dimensions** from the resume, such as:
    - Skills not mentioned
    - Learning style (online vs in-person)
    - Ideal job environment (hybrid, remote)
    - Work values or preferences
    - Do not use placeholders like [Insert answer here] or [Describe reason]. Write full, meaningful options for each question.
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

def generate_user_summary(answers):
    prompt = f"""
You are a career assistant AI.
You are given a user's multiple-choice survey answers. Your task is to:
1. Match each answer to one or more of these **predefined structured occupational skill categories** only:
{domain_instruction}
Return a JSON object structured as:
{{
  "structured_skills_from_survey": {{
    "Abilities": [...],
    "Knowledge": [...],
    "Skills": [...],
    "Work Activities": [...],
    "Work Context": [...],
    "Work Styles": [...],
    "Work Values": [...]
  }},
  "summary": "A 4–6 sentence description of the user's motivations, goals, and preferences based on their answers, including their time and budget for learning."
}}
Only include skills that exist in the provided lists — **do not invent new skills**. You can omit empty categories.

User’s survey answers:
{json.dumps(answers, indent=2)}
"""

    try:
        model = GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        cleaned_json = response.text.strip().lstrip("```json\n").rstrip("```").strip()
        result = json.loads(cleaned_json)
        return result
    except Exception as e:
        raise ValueError(f"Error generating user profile summary: {e}")
