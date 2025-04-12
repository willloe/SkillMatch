from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGODB_URI = os.getenv('MONGODB_URI')

class MongoDBClient:
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client['skillmatch_db']  # Database name as per your setup
    
    def insert_resume(self, data):
        resumes_collection = self.db['resumes']
        result = resumes_collection.insert_one(data)
        return result.inserted_id
    
    def insert_profile(self, data):
        profiles_collection = self.db['profiles']
        result = profiles_collection.insert_one(data)
        return result.inserted_id
    
    def find_resume(self, query):
        resumes_collection = self.db['resumes']
        return resumes_collection.find_one(query)
    
    def find_profile(self, query):
        profiles_collection = self.db['profiles']
        return profiles_collection.find_one(query)