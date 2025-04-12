import pdfplumber
import io  # For handling file streams

def parse_resume(file):
    if file.filename.endswith('.pdf'):
        with pdfplumber.open(io.BytesIO(file.read())) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text() or ''  # Extract text from each page
            return text.strip()
    elif file.filename.endswith('.txt'):
        return file.read().decode('utf-8').strip()
    else:
        raise ValueError('Unsupported file type. Only PDF and TXT are allowed.')