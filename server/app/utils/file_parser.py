import os
import pdfplumber
import io  # For handling file streams

def parse_resume(filepath):
    # Check if file exists
    if not os.path.exists(filepath):
        raise ValueError(f"File not found: {filepath}")
    
    # PDF Parsing
    if filepath.lower().endswith('.pdf'):
        try:
            with pdfplumber.open(filepath) as pdf:
                text = ''
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + '\n'
                return text.strip()
        except Exception as e:
            raise ValueError(f"Error parsing PDF file '{os.path.basename(filepath)}': {e}")

    # Optional: TXT fallback
    elif filepath.lower().endswith('.txt'):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            raise ValueError(f"Error reading text file '{os.path.basename(filepath)}': {e}")

    # Unsupported format
    else:
        raise ValueError(f"Unsupported file type for '{filepath}'. Only PDF or TXT are allowed.")