from pathlib import Path

def validate_upload(filename):
    if Path(filename).suffix.lower() not in {".txt", ".pdf"}:
        raise ValueError("Only TXT and PDF files are allowed")
