from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGODB_URI = os.getenv('MONGODB_URI')

class MongoDBClient:
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client['skillmatch_db']
    
    def insert_resume(self, data):
        return self.db['resumes'].insert_one(data).inserted_id

    def insert_profile(self, data):
        return self.db['profiles'].insert_one(data).inserted_id

    def find_resume(self, query):
        return self.db['resumes'].find_one(query)

    def find_profile(self, query):
        return self.db['profiles'].find_one(query)