def analyze_resume(text):
    # Placeholder logic — replace with Gemini API call later
    words = text.split()
    skills = [w for w in ["Python", "SQL", "Excel", "Java"] if w in text]
    return {
        "word_count": len(words),
        "skills": skills or ["No recognized skills found."]
    }