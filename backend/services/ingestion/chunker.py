import uuid

def make_chunks(sections, max_chars=450, overlap=90):
    result = []
    for section in sections:
        text = section["text"]
        parent_key = str(uuid.uuid4())
        parent_text = text
        start = 0
        while start < len(text):
            end = min(start + max_chars, len(text))
            piece = text[start:end].strip()
            if piece:
                result.append({
                    "chunk_key": str(uuid.uuid4()),
                    "parent_key": parent_key,
                    "page": section["page"],
                    "section": section["section"],
                    "content": piece,
                    "parent_content": parent_text
                })
            if end == len(text):
                break
            start = max(end - overlap, start + 1)
    return result
