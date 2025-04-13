import os
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai
from pinecone import Pinecone

class Similarity:
    def __init__(self):
        load_dotenv()
        self.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        self.PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

    def _get_embedding(self, text):
        try:
            genai.configure(api_key=self.GOOGLE_API_KEY)
            response = genai.embed_content(
                model="models/embedding-001",
                content=text,
                task_type="RETRIEVAL_DOCUMENT"
            )
            return response["embedding"]
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []

    def return_job(self, text):
        try:
            resume_embedding = self._get_embedding(text)
            pc = Pinecone(api_key=self.PINECONE_API_KEY)
            index = pc.Index("job-match")
            results = index.query(vector=resume_embedding, top_k=10, include_metadata=True)

            matched_jobs = []
            for match in results["matches"]:
                job_info = {
                    "score": round(match["score"], 5),
                    "title": match["metadata"].get("job_title", "Untitled Role"),
                    "skills": match["metadata"].get("job_skills", []),
                    "summary": match["metadata"].get("job_summary", "")
                }
                matched_jobs.append(job_info)

            return matched_jobs

        except Exception as e:
            print(f"Error querying job index: {e}")
            return []

    def return_course(self, text):
        try:
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

        except Exception as e:
            print(f"Error querying course index: {e}")
            return []

    def return_program(self, text):
        try:
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

        except Exception as e:
            print(f"Error querying program index: {e}")
            return []