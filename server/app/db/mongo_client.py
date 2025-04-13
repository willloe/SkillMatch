from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGODB_URI)
db = client["skillmatch_db"]
profiles_collection = db["profiles"]
resumes_collection = db["resumes"]


def save_resume_to_mongo(user_id, text, upload_time):
    resume_data = {
        "user_id": user_id,
        "text": text,
        "upload_time": upload_time,
    }
    result = resumes_collection.insert_one(resume_data)
    # print("✅ Resume saved with ID:", str(result))
    return result.inserted_id


def store_profile_basics(user_id, resume_text, top_skills, structured_skills, resume_db_id):
    try:
        result = profiles_collection.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "user_id": user_id,
                    "resume_text": resume_text,
                    "top_skills": top_skills,
                    "structured_skills": structured_skills,
                    "resume_db_id": resume_db_id,
                    "created_at": datetime.now(),
                }
            },
            upsert=True,
        )
        updated_profile = profiles_collection.find_one({"user_id": user_id})
        # print("✅ store_profile_basics: Updated Profile Object:")
        print(updated_profile["structured_skills"])

        return result.upserted_id or profiles_collection.find_one({"user_id": user_id})["_id"]
    except Exception as e:
        raise ValueError(f"Error saving profile basics: {e}")


def update_profile_with_survey(user_id, answers, categorized_answers, summary):
    try:
        result = profiles_collection.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "survey_answers": answers,
                    "categorized_answers": categorized_answers,
                    "career_summary": summary,
                    "updated_at": datetime.now(),
                }
            },
        )
        # updated_profile = profiles_collection.find_one({"user_id": user_id})
        # print("✅ update_profile_with_survey: Updated Profile Object:")
        # print(updated_profile["structured_skills"])
        # print(updated_profile["career_summary"])

        return result.modified_count
    except Exception as e:
        raise ValueError(f"Error updating profile with survey: {e}")


def get_profile_by_user_id(user_id):
    try:
        profile = profiles_collection.find_one({"user_id": user_id})
        return profile
    except Exception as e:
        print(f"❌ Error retrieving profile for user_id {user_id}: {e}")
        return None