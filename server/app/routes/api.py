from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import traceback
import datetime

from app.utils.user_id import get_or_create_user_id
from app.services.similiarity import Similarity
from app.utils.file_parser import parse_resume
from app.services.gemini_service import (
    extract_top_skills,
    extract_categorized_skills,
    generate_mcqs,
    generate_user_summary
)
from app.db.mongo_client import (
    save_resume_to_mongo, 
    store_profile_basics,
    update_profile_with_survey,
    get_profile_by_user_id
)


api = Blueprint('api', __name__)

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
        user_id = request.form.get('user_id') or get_or_create_user_id(request)
        upload_time = datetime.datetime.now()

        top_skills = extract_top_skills(resume_text)
        structured_skills = extract_categorized_skills(resume_text)
        resume_id = save_resume_to_mongo(user_id, resume_text, upload_time)
        profile_id = store_profile_basics(user_id, resume_text, top_skills, structured_skills, resume_id)

        questions = generate_mcqs(resume_text, top_skills, structured_skills)

        return jsonify({
            "success": True,
            "user_id": user_id,
            "file_received": filename,
            "resume_db_id": str(resume_id),
            "profile_db_id": str(profile_id),
            "questions": questions
        }), 200

    except Exception as e:
        print("Upload Error:", str(e))
        traceback.print_exc()
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500
    
@api.route("/submit-answers", methods=["POST"])
def submit_answers():
    try:
        data = request.get_json()
        user_id = data.get('user_id') or get_or_create_user_id(request)
        
        print("1UserId:" + str(user_id))
        answers = data.get("answers", {})

        if not isinstance(answers, dict):
            return jsonify({"error": "Invalid answers format"}), 400

        categorized, summary = generate_user_summary(answers)

        # Store answers
        update_profile_with_survey(user_id, answers, categorized, summary)


        # Simple placeholder for recommendations
        recommendations = run_recommendation_model(user_id)
        
        print("***Recommendations:")
        print(recommendations)

        return jsonify({
            "success": True,
            "recommendations": recommendations
        })

    except Exception as e:
        print("Submit Error:", e)
        return jsonify({"error": str(e)}), 500

def run_recommendation_model(user_id):
    try:
        if not user_id:
            print("Error1: No user_id provided")
            return []
        print("UserId:" + str(user_id))
        profile = get_profile_by_user_id(user_id)
        if not profile:
            print("Error2: No profile found for user_id:", user_id)
            return []

        resume_text = profile.get("resume_text", "")
        sim = Similarity()
        jobs = sim.return_job(resume_text)

        return jobs

    except Exception as e:
        traceback.print_exc()
        print("Error3:", e)
        return []
    
@api.route("/selected-job", methods=["POST"])
def selected_job():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data received"}), 400

        user_id = data.get("user_id")
        selected_job = data.get("selected_job")
        if not user_id or not selected_job:
            return jsonify({"error": "Missing user_id or selected_job"}), 400

        profile = get_profile_by_user_id(user_id)
        if not profile:
            return jsonify({"error": "User profile not found"}), 404

        # Get user skills from structured_skills (flatten all domains into one set)
        user_skills = set()
        for skill_list in profile.get("structured_skills", {}).values():
            if isinstance(skill_list, list):
                user_skills.update(s.strip().lower() for s in skill_list if isinstance(s, str))

        # Extract job skills (comma-separated string expected)
        job_skills_raw = selected_job.get("skills", "")
        job_skills = set(s.strip().lower() for s in job_skills_raw.split(",") if s.strip())

        # Identify missing skills
        missing_skills = list(job_skills - user_skills)
        print("Skill gap:", missing_skills)

        # Run course and program recommendations
        sim = Similarity()
        gap_text = ", ".join(missing_skills)
        course_recs = sim.return_course(gap_text)
        program_recs = sim.return_program(gap_text)

        return jsonify({
            "success": True,
            "skill_gap": missing_skills,
            "recommended_courses": course_recs,
            "recommended_programs": program_recs,
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Error handling selected job: {e}"}), 500