from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime

from app.utils.file_parser import parse_resume
from app.services.embedding import generate_and_store_embeddings
from app.services.questions import generate_questions
from app.db.mongo_client import MongoDBClient

api = Blueprint('api', __name__)
mongo = MongoDBClient()

@api.route("/upload", methods=["POST"])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No resume file uploaded"}), 400

    file = request.files['resume']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        # Parse text from file
        resume_text = parse_resume(file)
        user_id = request.form.get('user_id', 'test_user')

        # Save to MongoDB
        resume_id = mongo.insert_resume({
            'user_id': user_id,
            'text': resume_text,
            'upload_time': datetime.utcnow()
        })

        # Enrich with embeddings and questions
        embedding_id = generate_and_store_embeddings(resume_text, user_id)
        top_skills = ["Python", "SQL", "Excel"]
        questions = generate_questions(resume_text, top_skills)

        return jsonify({
            "success": True,
            "resume_id": str(resume_id),
            "embeddings": str(embedding_id),
            "questions": questions
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500