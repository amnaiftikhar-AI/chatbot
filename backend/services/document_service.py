import uuid
from pathlib import Path
from backend.models import Document, Chunk
from backend.services.ingestion.file_loader import load_file
from backend.services.ingestion.structure_extractor import extract_sections
from backend.services.ingestion.chunker import make_chunks
from backend.services.ingestion.metadata_extractor import extract_metadata
from backend.services.retrieval.hybrid_retriever import retriever

UPLOAD_DIR = Path("data/knowledge_base/raw")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def ingest_path(db, path, original_name=None):
    pages = load_file(str(path))
    full_text = "\n".join(page["text"] for page in pages)
    metadata = extract_metadata(full_text, original_name or Path(path).name)
    existing = db.query(Document).filter(Document.document_key == metadata["document_key"]).first()
    if existing:
        db.delete(existing)
        db.commit()
    document = Document(
        document_key=metadata["document_key"],
        filename=original_name or Path(path).name,
        title=metadata["title"],
        document_type=metadata["document_type"],
        device_model=metadata["device_model"],
        software_version=metadata["software_version"],
        category=metadata["category"],
        status=metadata["status"]
    )
    db.add(document)
    db.flush()
    chunks = make_chunks(extract_sections(pages))
    for item in chunks:
        db.add(Chunk(
            chunk_key=item["chunk_key"],
            document_id=document.id,
            parent_key=item["parent_key"],
            page_number=item["page"],
            section=item["section"],
            content=item["content"],
            parent_content=item["parent_content"]
        ))
    db.commit()
    retriever.rebuild()
    return document

def delete_document(db, document_id):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        return False
    db.delete(document)
    db.commit()
    retriever.rebuild()
    return True
