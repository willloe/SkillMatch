from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import datetime

from pymongo import MongoClient
from app.utils.file_parser import parse_resume
from app.db.save_resume import save_resume_to_mongo
from app.services.gemini_service import (
    extract_top_skills,
    extract_categorized_skills,
    generate_mcqs,
    generate_and_store_embeddings
)


api = Blueprint('api', __name__)

# Mongo connection for answers
mongo_client = MongoClient(os.getenv("MONGODB_URI"))
db = mongo_client['skillmatch_db']
answers_collection = db['survey_responses']

@api.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No resume file uploaded"}), 400

    file = request.files['resume']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        resume_text = parse_resume(filepath)
        user_id = request.form.get('user_id', 'test_user')
        upload_time = datetime.datetime.now()

        top_skills = extract_top_skills(resume_text)
        structured_skills = extract_categorized_skills(resume_text)
        resume_id = save_resume_to_mongo(user_id, resume_text, upload_time)
        profile_id = generate_and_store_embeddings(
            text=resume_text,
            user_id=user_id,
            top_skills=top_skills,
            structured_skills=structured_skills
        )
        questions = generate_mcqs(resume_text, top_skills, structured_skills)

        return jsonify({
            "success": True,
            "file_received": filename,
            "resume_db_id": str(resume_id),
            "profile_db_id": str(profile_id),
            "questions": questions
        }), 200

    except Exception as e:
        print("❌ Upload Error:", str(e))
        traceback.print_exc()  # ✅ full stack trace
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500
    
@api.route("/submit-answers", methods=["POST"])
def submit_answers():
    try:
        data = request.get_json()
        user_id = data.get("user_id", "anonymous")
        answers = data.get("answers", {})

        if not isinstance(answers, dict):
            return jsonify({"error": "Invalid answers format"}), 400

        # Store answers
        answers_collection.insert_one({
            "user_id": user_id,
            "answers": answers,
            "timestamp": datetime.datetime.now()
        })

        # Simple placeholder for recommendations
        recommendations = run_recommendation_model(answers)

        return jsonify({
            "success": True,
            "recommendations": recommendations
        })

    except Exception as e:
        print("❌ Submit Error:", e)
        return jsonify({"error": str(e)}), 500

def run_recommendation_model(answers):
    # 💡 Simple placeholder logic
    response = []

    for value in answers.values():
        if isinstance(value, str) and "data" in value.lower():
            response.append("📊 Take Data Analysis with Python (Coursera, Free)")
        elif "project" in value.lower():
            response.append("📁 Explore Project Management Certificate (Google)")
        elif "ml" in value.lower() or "machine" in value.lower():
            response.append("🤖 Enroll in FastAI ML Bootcamp")

    return response or ["📚 Try Exploring LinkedIn Learning Paths"]