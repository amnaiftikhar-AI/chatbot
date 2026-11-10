from backend.services.retrieval.faiss_store import FaissStore
from backend.services.retrieval.bm25_store import BM25Store
from backend.services.retrieval.rrf import reciprocal_rank_fusion, deduplicate
from backend.db.database import SessionLocal
from backend.models import Chunk, Document

class HybridRetriever:
    def __init__(self):
        self.faiss = FaissStore()
        self.bm25 = BM25Store()
        self.items = []

    def rebuild(self):
        db = SessionLocal()
        try:
            rows = db.query(Chunk, Document).join(Document).filter(Document.status != "deleted").all()
            items = []
            for chunk, document in rows:
                items.append({
                    "chunk_key": chunk.chunk_key,
                    "document_id": document.id,
                    "filename": document.filename,
                    "title": document.title,
                    "page": chunk.page_number,
                    "section": chunk.section,
                    "content": chunk.content,
                    "metadata": {
                        "document_type": document.document_type,
                        "device_model": document.device_model,
                        "software_version": document.software_version,
                        "category": document.category,
                        "status": document.status
                    }
                })
            self.items = items
            self.faiss.build(items)
            self.bm25.build(items)
            self.faiss.save()
        finally:
            db.close()

    def search(self, query, k=8):
        if not self.items:
            self.rebuild()
        dense = self.faiss.search(query, k)
        sparse = self.bm25.search(query, k)
        return deduplicate(reciprocal_rank_fusion([dense, sparse])[:k])

retriever = HybridRetriever()
