from backend.services.ingestion.chunker import make_chunks

def test_chunker_returns_content():
    chunks = make_chunks([{"page": 1, "section": "Test", "text": "A" * 1500}], max_chars=500, overlap=50)
    assert len(chunks) > 1
    assert all(item["content"] for item in chunks)
