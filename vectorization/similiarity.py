import os
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai
from pinecone import Pinecone, ServerlessSpec
import json

class similiarity:
    def __init__(self):
        load_dotenv()
        self.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        self.PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

    def _get_embedding(self, text):
        genai.configure(api_key=self.GOOGLE_API_KEY)
        response = genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="RETRIEVAL_DOCUMENT"
        )
        return response["embedding"]

    def return_job(self, text):
        # Query Pinecone for top 3 matching jobs
        resume_embedding = self._get_embedding(text)
        pc = Pinecone(api_key=self.PINECONE_API_KEY)
        index_name = "job-match"
        index = pc.Index(index_name)
        results = index.query(vector=resume_embedding, top_k=10, include_metadata=True)

        matched_jobs = []

        # Display matching job postings
        for match in results["matches"]:
            print(f"\nScore: {match['score']:.4f}")
            print(f"Job Title: {match['metadata']['job_title']}")
            print(f"Skills: {match['metadata']['job_skills']}")
            print(f"Description: {match['metadata']['job_summary']}")

        return matched_jobs
    
    def return_course(self, text):
        # Query Pinecone for top 3 matching courses
        course_embedding = self._get_embedding(text)
        pc = Pinecone(api_key=self.PINECONE_API_KEY)
        index = pc.Index("course-matching")
        results = index.query(vector=course_embedding, top_k=3, include_metadata=True)

        matched_courses = []

        for match in results["matches"]:
            course_info = {
                "score": round(match["score"], 4),
                "title": match["metadata"].get("title", ""),
                "summary": match["metadata"].get("summary", ""),
                "url": match["metadata"].get("url", ""),
                "query": match["metadata"].get("query", "")
            }
            matched_courses.append(course_info)

        return matched_courses
    
    def return_program(self, text):
        # Query Pinecone for top 3 matching programs
        program_embedding = self._get_embedding(text)
        pc = Pinecone(api_key=self.PINECONE_API_KEY)
        index = pc.Index("program-match")
        results = index.query(vector=program_embedding, top_k=3, include_metadata=True)

        matched_programs = []

        for match in results["matches"]:
            program_info = {
                "score": round(match["score"], 4),
                "university": match["metadata"].get("INSTNM", ""),
                "cip_description": match["metadata"].get("CIPDESC", ""),
                "degree_level": match["metadata"].get("CREDDESC", ""),
                "cip_code": match["metadata"].get("CIPCODE", "")
            }
            matched_programs.append(program_info)

        return matched_programs



        






        