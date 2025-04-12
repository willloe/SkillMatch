from pymongo import MongoClient
import os
from dotenv import load_dotenv
import datetime

load_dotenv()
MONGODB_URI = os.getenv('MONGODB_URI')

client = MongoClient(MONGODB_URI)
db = client['skillmatch_db']
resumes_collection = db['resumes']

def save_resume_to_mongo(user_id, text, upload_time=None):
    if upload_time is None:
        upload_time = datetime.datetime.now()

    resume_data = {
        'user_id': user_id,
        'text': text,
        'upload_time': upload_time
    }
    result = resumes_collection.insert_one(resume_data)
    return result.inserted_id