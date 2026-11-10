from pathlib import Path
from pypdf import PdfReader

def load_file(path: str):
    file_path = Path(path)
    if file_path.suffix.lower() == ".txt":
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        return [{"page": 1, "text": text}]
    if file_path.suffix.lower() == ".pdf":
        reader = PdfReader(str(file_path))
        return [{"page": number, "text": page.extract_text() or ""} for number, page in enumerate(reader.pages, 1)]
    raise ValueError("Only PDF and TXT files are supported")
