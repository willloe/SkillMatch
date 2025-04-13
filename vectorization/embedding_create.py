import os
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai
from pinecone import Pinecone, ServerlessSpec
import json

class embedd:
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
    
    def _create_index(self, index_name):
        pc = Pinecone(api_key=self.PINECONE_API_KEY)
                # Create index if it doesn't exist
        if index_name not in pc.list_indexes().names():
            pc.create_index(
                name=index_name,
                dimension=768,  # Adjust based on your embedding dimension
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")  # Adjust based on your needs
            )

    def add_job(self):
        pc = Pinecone(api_key=self.PINECONE_API_KEY)
        index_name = "job-match"
        self._create_index(index_name)

        index = pc.Index(index_name)

        df = pd.read_csv("merged_output.csv")

                # Ensure job_id is a string
        df.dropna(inplace=True)  # Drop rows with NaN values
        df["job_id"] = df.index.astype(str)

        for _, row in df.iterrows():
            combined_text = f"{row['job_title']} {row['job_skills']} {row['job_summary']}"
            embedding = self._get_embedding(combined_text)
            index.upsert([(row['job_id'], embedding, row.to_dict())])

    def add_program(self):
        index_name = "program-match"
        pc = Pinecone(api_key=self.PINECONE_API_KEY)

        columns_to_load = [
            "UNITID", "OPEID6", "INSTNM", "CONTROL", "MAIN",
            "CIPCODE", "CIPDESC", "CREDLEV", "CREDDESC"
        ]



        # Load only the selected columns
        df = pd.read_csv("dmv_universities.csv", usecols=columns_to_load)

        df.dropna(inplace=True)  # Drop rows with NaN values
        df["row_id"] = df.index.astype(str)

        self._create_index(index_name)
        index = pc.Index(index_name)

        for _, row in df.iterrows():
            text_to_embed = f"{row['CIPDESC']} - {row['CREDDESC']}"
            embedding = self._get_embedding(text_to_embed)
            metadata = row.to_dict()
            index.upsert([(str(row['row_id']), embedding, metadata)])

        print("Program data embedded and stored in 'program-matching' index.")

    def add_course(self):
        with open("courses_summary_by_query.json", "r", encoding="utf-8") as f:
            course_list = json.load(f)

        df = pd.DataFrame(course_list)

        df.dropna(inplace=True)  # Drop rows with NaN values
        df["row_id"] = df.index.astype(str)

        # Initialize Pinecone
        pc = Pinecone(api_key=self.PINECONE_API_KEY)
        index_name = "course-matching"

        self._create_index(index_name)

        index = pc.Index(index_name)

        # Embed and upsert all courses
        for course in course_list:
            combined_text = f"{course['title']} {course['summary']}"
            embedding = self._get_embedding(combined_text)
            index.upsert([
                (course['url'], embedding, course)
            ])
            print(f"Upserted: {course['title'][:60]}...")

        print(f"\nSuccessfully stored {len(course_list)} courses in Pinecone!")



