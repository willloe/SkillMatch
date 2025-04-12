import json  # For returning questions as JSON
import random
# Import not needed since we're not using generate_and_store_embeddings in this file

# Predefined questions based on TASKS.md
def generate_questions(embeddings, top_skills):
    questions = [
        {"text": "Which skill would you like to learn next?", "options": [f"A) {top_skills[0] if len(top_skills) > 0 else 'SQL'}", f"B) {top_skills[1] if len(top_skills) > 1 else 'Python'}", f"C) {top_skills[2] if len(top_skills) > 2 else 'Excel'}", "D) None"]},
        {"text": "What is your preferred skill to improve?", "options": [f"A) {top_skills[0] if len(top_skills) > 0 else 'SQL'}", f"B) {top_skills[1] if len(top_skills) > 1 else 'Python'}", f"C) {top_skills[2] if len(top_skills) > 2 else 'Excel'}", "D) Other"]},
        {"text": "Which skill do you want to prioritize?", "options": [f"A) {top_skills[0] if len(top_skills) > 0 else 'SQL'}", f"B) {top_skills[1] if len(top_skills) > 1 else 'Python'}", f"C) {top_skills[2] if len(top_skills) > 2 else 'Excel'}", "D) None"]},
        # Career goals (questions 4-6)
        {"text": "What role are you aiming for?", "options": ["A) Data Analyst", "B) Developer", "C) Manager", "D) Other"]},
        {"text": "What is your career aspiration?", "options": ["A) Technical Role", "B) Leadership Role", "C) Creative Role", "D) Flexible"]},
        {"text": "Which industry interests you most?", "options": ["A) Tech", "B) Finance", "C) Healthcare", "D) Other"]},
        # Location (questions 7-8)
        {"text": "Where do you prefer to work?", "options": ["A) Maryland", "B) Remote", "C) Other State", "D) Flexible"]},
        {"text": "What is your ideal work location?", "options": ["A) In-Person", "B) Hybrid", "C) Fully Remote", "D) No Preference"]},
        # Learning style (questions 9-10)
        {"text": "What is your preferred learning format?", "options": ["A) Online", "B) In-Person", "C) Hybrid", "D) Self-Paced"]},
        {"text": "How do you like to learn new skills?", "options": ["A) Courses", "B) Hands-On", "C) Reading", "D) Group Sessions"]}
    ]
    return json.dumps({"questions": questions})  # Return as JSON string 